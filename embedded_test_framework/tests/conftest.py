import pytest
import os
from src.test_framework.t32_connector import T32Connector
from src.test_framework.config_loader import load_config

@pytest.fixture(scope="session")
def t32_session():
    """Session-scoped fixture to manage T32 connection using config."""
    print("\nSetting up T32 session using configuration...")
    
    try:
        cfg = load_config("global_settings.ini")
        # Get values from config, with environment variable overrides
        node = os.environ.get("T32_NODE", cfg.get('Trace32', 'node', fallback='localhost'))
        port = os.environ.get("T32_PORT", cfg.get('Trace32', 'port', fallback='20000'))
        api_dll_path_cfg = cfg.get('Trace32', 'api_dll_path', fallback=None)
        t32_api_path = api_dll_path_cfg if api_dll_path_cfg and api_dll_path_cfg.strip() else None
        
        # Get retry parameters from environment or config
        max_retries = int(os.environ.get("T32_MAX_RETRIES", "1"))
        retry_delay = float(os.environ.get("T32_RETRY_DELAY", "1.0"))

    except Exception as e:
        pytest.fail(f"Failed to load configuration for t32_session: {e}")

    connector = T32Connector(t32_api_path=t32_api_path)
    if not connector.t32_lib:
        pytest.fail(f"T32 API library failed to load in fixture (path from config: {t32_api_path}).")

    connected = connector.connect(node=node, port=port, max_retries=max_retries, retry_delay=retry_delay)
    if not connected:
        pytest.fail(f"Failed to connect to Trace32 ({node}:{port}) in fixture.")
    
    yield connector

    print("\nTearing down T32 session...")
    connector.disconnect() 