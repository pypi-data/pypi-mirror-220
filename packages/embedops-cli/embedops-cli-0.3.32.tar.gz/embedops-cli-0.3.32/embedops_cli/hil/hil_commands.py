"""
Contains functions for the HIL sub-group commands.
"""

import json
import os.path
import tempfile
import click
from embedops_cli.eo_types import (
    EmbedOpsException,
    NoRepoIdException,
    NetworkException,
    LoginFailureException,
    UnauthorizedUserException,
)
from embedops_cli.api.rest import ApiException
from embedops_cli.hil.hil_common import get_hil_sdk_path
from embedops_cli.hil.hil_types import (
    NoHILSDKPathException,
    HILRepoId404Exception,
    HILSDKPathDoesNotExistException,
    HILPackageCreationException,
)
from embedops_cli.hil.hil_package import create_hil_package
from embedops_cli.sse.sse_api import SSEApi
from embedops_cli.sse import eo_sse
from embedops_cli.utilities import echo_error_and_fix
from embedops_cli import embedops_authorization
from embedops_cli import config
from embedops_cli.hil import hil_package


@click.command()
@click.pass_context
def blink(ctx: click.Context):

    """Get a streaming response for the given event feed using urllib3."""

    try:

        repo_id = config.get_repo_id()

        if not repo_id:
            raise NoRepoIdException()

        sse_api = SSEApi()
        for event in sse_api.sse_blink_gateway(repo_id):
            if event.event == eo_sse.SSE_TEXT_EVENT:
                eo_sse.sse_print_command_text(event)
            elif event.event == eo_sse.SSE_RESULT_EVENT:
                result_event_obj = json.loads(event.data)
                ctx.exit(result_event_obj["exitCode"])
            else:
                pass  # Just ignore

        # If the command hasn't returned anything yet, exit here
        ctx.exit(2)

    except NoRepoIdException as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except NetworkException as exc:
        if exc.status_code == 401:
            echo_error_and_fix(LoginFailureException())
        elif exc.status_code == 404:
            echo_error_and_fix(HILRepoId404Exception())
        else:
            echo_error_and_fix(exc)

        ctx.exit(2)


@click.command()
@click.pass_context
def run(ctx: click.Context):

    """Run hil in local mode, using the current repository as a source."""

    try:

        repo_id = config.get_repo_id()
        if not repo_id:
            raise NoRepoIdException()

        hil_sdk_path = get_hil_sdk_path()
        if not hil_sdk_path:
            raise NoHILSDKPathException()

        hil_sdk_full_path = os.path.join(os.path.curdir, hil_sdk_path)
        if not os.path.isdir(hil_sdk_full_path):
            raise HILSDKPathDoesNotExistException()

        # Compile the package in a temporary folder that is deleted after uploading
        with tempfile.TemporaryDirectory() as tmp_dir:

            hil_ep_file = os.path.join(tmp_dir, "hil_ep.zip")

            # TODO: Build artifacts and manifest data are being left blank intentionally
            if not create_hil_package([], hil_sdk_path, {}, hil_ep_file):
                raise HILPackageCreationException()

            # Get the upload URL
            api_client = embedops_authorization.get_user_client()
            upload_url_response = api_client.get_pre_signed_url_for_upload(repo_id)
            upload_url = upload_url_response.url

            click.echo("Uploading HIL execution package...")
            upload_status = hil_package.upload_hil_package(hil_ep_file, upload_url)
            if upload_status != 200:
                raise NetworkException(
                    upload_status,
                    message="network exception during execution package upload",
                )

        # After package is uploaded, call into SSE and print any further events
        sse_api = SSEApi()
        for event in sse_api.sse_hil_run(repo_id):
            if event.event == eo_sse.SSE_TEXT_EVENT:
                eo_sse.sse_print_command_text(event)
            elif event.event == eo_sse.SSE_RESULT_EVENT:
                result_event_obj = json.loads(event.data)
                ctx.exit(result_event_obj["exitCode"])
            else:
                pass  # Just ignore

        # If the command hasn't returned anything yet, exit here
        ctx.exit(2)

    except (
        NoRepoIdException,
        NoHILSDKPathException,
        HILSDKPathDoesNotExistException,
        HILPackageCreationException,
        NetworkException,
        UnauthorizedUserException,
    ) as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except ApiException:
        echo_error_and_fix(
            EmbedOpsException(fix_message="Uploading the HIL execution package failed.")
        )
