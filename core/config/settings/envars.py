from core.core.utils.settings import get_settings_from_environment
from khatabook_v1.core.core.utils.collections_utl import deep_update

# globals() is the dictionary of global variables
deep_update(
    globals(),
    get_settings_from_environment(ENV_SETTINGS_PREFIX),  # type ignore # noqa: F821
)  # type ignore # noqa: F821
