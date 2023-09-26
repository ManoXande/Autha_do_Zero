#configurations.py
import locale

# Logging settings
LOG_TO_TERMINAL = False

# Default rounding rules
ROUNDING_RULES = {
    "coordinates": 3,
    "distances": 2,
    "azimuths": 2
}

# Default memorial and table templates
DEFAULT_MEMORIAL_TEMPLATE = "Chapeco_SC"
DEFAULT_TABLE_TEMPLATE = "Chapeco_SC"

def set_rounding_rules(coord_decimals=2, distance_decimals=2, azimuth_decimals=2):
    """Update the rounding rules"""
    global ROUNDING_RULES
    ROUNDING_RULES = {
        "coordinates": coord_decimals,
        "distances": distance_decimals,
        "azimuths": azimuth_decimals
    }

def set_memorial_template(template_name):
    """Update the default memorial template"""
    global DEFAULT_MEMORIAL_TEMPLATE
    DEFAULT_MEMORIAL_TEMPLATE = template_name

def set_table_template(template_name):
    """Update the default table template"""
    global DEFAULT_TABLE_TEMPLATE
    DEFAULT_TABLE_TEMPLATE = template_name

def set_locale(region="pt_BR"):
    """Set the locale"""
    try:
        locale.setlocale(locale.LC_ALL, region)
    except locale.Error:
        print(f"Locale {region} not found. Using default.")

def set_coordinate_system(epsg_code):
    """Set the EPSG code for the coordinate system (implementation needed)"""
    return 

def set_debug_mode(active=False):
    """Turn debug mode on or off (implementation needed)"""
    pass

def set_logging_to_terminal(active=False):
    """Enable or disable logging to terminal"""
    global LOG_TO_TERMINAL
    LOG_TO_TERMINAL = active

def log(message):
    """Log a message to the terminal if logging is enabled"""
    if LOG_TO_TERMINAL:
        print(message)

def get_logging_level():
    # Implementação da função
    pass
