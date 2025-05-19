import pytest
from src.test_framework.t32_connector import T32Connector
from src.test_framework.config_loader import load_config

@pytest.fixture(scope="session")
def t32_session():
    """Session-scoped fixture to manage T32 connection using config."""
    print("\nSetting up T32 session using configuration...")
    
    try:
        cfg = load_config("global_settings.ini")
        node = cfg.get('Trace32', 'node', fallback='localhost')
        port = cfg.get('Trace32', 'port', fallback='20000')
        api_dll_path_cfg = cfg.get('Trace32', 'api_dll_path', fallback=None)
        # Use the path from config if it's not empty, otherwise pass None
        t32_api_path = api_dll_path_cfg if api_dll_path_cfg and api_dll_path_cfg.strip() else None

    except Exception as e:
        pytest.fail(f"Failed to load configuration for t32_session: {e}")

    connector = T32Connector(t32_api_path=t32_api_path)
    if not connector.t32_lib:
        pytest.fail(f"T32 API library failed to load in fixture (path from config: {t32_api_path}).")

    connected = connector.connect(node=node, port=port)
    if not connected:
        pytest.fail(f"Failed to connect to Trace32 ({node}:{port}) in fixture.")
    
    yield connector

    print("\nTearing down T32 session...")
    connector.disconnect() 