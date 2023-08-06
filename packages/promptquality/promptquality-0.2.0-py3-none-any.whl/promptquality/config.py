from typing import Optional

from promptquality.constants.config import ConfigDefaults
from promptquality.types.config import Config
from promptquality.utils.config import _config_location, set_console_url


def set_config(console_url: Optional[str] = None) -> Config:
    if _config_location().exists():
        config = Config.read()
    else:
        console_url = console_url or ConfigDefaults.console_url
        set_console_url(console_url=console_url)
        config = Config(console_url=console_url)
    config.write()
    return config
