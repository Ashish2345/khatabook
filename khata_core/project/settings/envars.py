from utils.collections_utl import deep_update
from utils.settings_utl import get_settings_from_environment

# globals() is the dictionary of global variables
deep_update(
    globals(),
    get_settings_from_environment(ENV_SETTINGS_PREFIX),  # type ignore # noqa: F821
)  # type ignore # noqa: F821
