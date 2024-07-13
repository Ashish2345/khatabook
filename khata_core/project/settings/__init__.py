import os.path

from split_settings.tools import include, optional


# Namespacing out own custom environement variables


ENV_SETTINGS_PREFIX = "CORESETTINGS"

LOCAL_SETTINGS_PATH = os.getenv(f"{ENV_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings_example.dev.py"

# if not os.path.isabs(LOCAL_SETTINGS_PATH):
#     LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)


# Include Various settings files and aggrigate as one

include("base.py", "custom.py", optional(LOCAL_SETTINGS_PATH), "envars.py")
