"""
The hil_package library includes functions for creating and extracting HIL execution packages.
These packages are ZIP-based and contain the build artifacts, HIL tests, and metadata for a
given HIL run.
"""
import os
import tempfile
import shutil
import json
import logging
import requests


_logger = logging.getLogger(__name__)

# The fixed name of the HIL manifest file
HIL_MANIFEST_NAME = "hil_manifest.json"

# Passed to the shutil.make_archive tool
HIL_ARCHIVE_FORMAT = "zip"


def create_hil_package(
    build_artifacts: list[str], hil_directory: str, manifest_data: dict, out_path: str
) -> bool:

    """

    Build a HIL execution package archive. The inputs are copied to a temporary directory
    prior to zipping.

    :param build_artifacts: A list of paths to files that are considered build artifacts
    :param hil_directory: Path to the repository's hil root directory
    :param manifest_data: Dictionary of data that will be inserted into the package's
    manifest JSON file (eg, Git data)
    :param out_path: Full output path of the package, including the file name
    :return: True if success; False otherwise
    """

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Copy all artifacts into temporary dir
        artifacts_path = os.path.join(tmp_dir, "artifacts")
        os.mkdir(artifacts_path)
        for artifact in build_artifacts:

            artifact_name = os.path.basename(artifact)

            if os.path.isfile(artifact):
                shutil.copyfile(artifact, os.path.join(artifacts_path, artifact_name))
            else:
                return False

        # Copy in the HIL directory
        shutil.copytree(
            hil_directory, os.path.join(tmp_dir, os.path.basename(hil_directory))
        )

        # Write the manifest file
        with open(
            os.path.join(tmp_dir, HIL_MANIFEST_NAME), "w", encoding="utf-8"
        ) as m_file:
            json.dump(manifest_data, m_file, indent=4)

        # Create the actual archive file
        out_archive_path = os.path.splitext(out_path)[0]
        shutil.make_archive(out_archive_path, HIL_ARCHIVE_FORMAT, tmp_dir)

    # Only return success if the outfile exists
    if os.path.isfile(out_path):
        return True

    return False


def upload_hil_package(package_path: str, url: str) -> bool:

    """
    Upload a HIL package ZIP to the given S3 bucket pre-signed URL. This function assumes
    that the file exists.
    """

    headers = {
        "Content-Type": "application/zip",
        "x-amz-server-side-encryption": "AES256",
    }

    with open(package_path, "rb") as archive_file:
        data = archive_file.read()
        response = requests.put(  # pylint: disable=W3101
            url,
            headers=headers,
            data=data,
        )

        _logger.debug(f"HIL package upload response: {str(response)}\n")

    return response.status_code
