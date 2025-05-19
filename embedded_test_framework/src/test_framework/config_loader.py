import configparser
import os

def load_config(config_file_name="global_settings.ini"):
    """Loads configuration from an INI file."""
    # Assume config dir is one level up from src/test_framework/ and then into config/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir_path = os.path.join(current_dir, "..", "..", "config")
    config_file_path = os.path.join(config_dir_path, config_file_name)

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file not found: {config_file_path}")

    parser = configparser.ConfigParser()
    parser.read(config_file_path)
    return parser 