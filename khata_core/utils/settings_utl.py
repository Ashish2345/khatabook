import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    """
    Gets the environment variables from system or docker like
    CORESETTINGS_IN_DOCKER and then slice this prefix CORESETTINGS_.

    returns (dict): text without the prefix: dict
    """

    prefix_len = len(prefix)
    return {
        key[prefix_len:]: yaml_coerce(val)
        for key, val in os.environ.items()
        if key.startswith(prefix)
    }
