from typing import Optional

from promptquality.constants.config import ConfigDefaults
from promptquality.types.config import Config
from promptquality.utils.config import _config_location, set_console_url


def set_config(console_url: Optional[str] = None) -> Config:
    """
    Set the config for `promptquality`.

    If the config file exists, and console_url is not passed, read it and return the
    config. Otherwise, set the default console URL and return the config.

    Parameters
    ----------
    console_url : Optional[str], optional
        URL to the Galileo console, by default None and we use the Galileo Cloud URL.

    Returns
    -------
    Config
        Config object for `promptquality`.
    """
    if not console_url and _config_location().exists():
        config = Config.read()
    else:
        console_url = console_url or ConfigDefaults.console_url
        set_console_url(console_url=console_url)
        config = Config(console_url=console_url)
    config.write()
    return config
