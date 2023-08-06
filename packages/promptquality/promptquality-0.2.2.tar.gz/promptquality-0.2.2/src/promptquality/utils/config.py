from os import environ, getenv
from pathlib import Path

from promptquality.constants.config import ConfigDefaults, ConfigEnvironmentVariables


def _config_location() -> Path:
    return Path.home().joinpath(
        ConfigDefaults.config_directory, ConfigDefaults.config_filename
    )


def set_console_url(console_url: str) -> None:
    """For Enterprise users. Set the console URL to your Galileo Environment.

    You can also set GALILEO_CONSOLE_URL before importing promptquality to bypass this

    :param console_url: If set, that will be used. Otherwise, if an environment variable
    GALILEO_CONSOLE_URL is set, that will be used. Otherwise, you will be prompted for
    a url.
    """
    if getenv(ConfigEnvironmentVariables.console_url, None) is None:
        environ[ConfigEnvironmentVariables.console_url] = console_url
