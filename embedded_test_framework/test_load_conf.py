from src.test_framework.config_loader import load_config

try:
    config = load_config()
    print(f"Node: {config['Trace32']['node']}")
    print(f"Port: {config['Trace32']['port']}")
    api_path = config.get('Trace32', 'api_dll_path', fallback=None)
    if api_path:  # Only print if it's not empty
        print(f"API DLL Path: {api_path}")
    else:
        print("API DLL Path: Not specified, relying on system PATH.")

except Exception as e:
    print(f"Error loading config: {e}") 