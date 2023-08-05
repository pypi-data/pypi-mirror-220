"""Common functions used by the HIL commands"""
from dynaconf import Dynaconf
from embedops_cli.hil.hil_types import get_hil_config_path


def get_hil_sdk_path():
    """get hil_sdk_path from .embedops/hil/config.yml

    Returns:
        str: the value stored in <repo_root>/.embedops/hil/config.yml:hil_sdk_path or None
    """
    dot_eo = Dynaconf(
        load_dotenv=False,
        settings_files=[get_hil_config_path()],
        silent_errors=True,
    )
    dot_eo.configure(
        LOADERS_FOR_DYNACONF=[
            "dynaconf.loaders.yaml_loader",
        ]
    )
    return dot_eo.get("hil_sdk_path")
