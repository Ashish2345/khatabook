from core.core.utils.collections import deep_update
from core.core.utils.settings import get_settings_from_environment


# globals() is the dictionary of global variables
deep_update(globals(), get_settings_from_environment(ENV_SETTINGS_PREFIX))