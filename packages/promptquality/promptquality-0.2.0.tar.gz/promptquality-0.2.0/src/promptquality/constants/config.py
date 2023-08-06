from types import SimpleNamespace

ConfigDefaults = SimpleNamespace(
    console_url="https://console.cloud.rungalileo.io/",
    config_directory=".galileo",
    config_filename="pq-config.json",
)


ConfigEnvironmentVariables = SimpleNamespace(
    console_url="GALILEO_CONSOLE_URL",
    username="GALILEO_USERNAME",
    password="GALILEO_PASSWORD",
)
