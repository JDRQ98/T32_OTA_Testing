import pytest
from src.test_framework.t32_connector import T32Connector

# Hardcode T32 API path for now for the fixture, or ensure it's in system PATH
T32_API_DLL_PATH = None  # Let it try to find in PATH by default

@pytest.fixture(scope="session")
def t32_session():
    """Session-scoped fixture to manage T32 connection."""
    print("\nSetting up T32 session...")
    connector = T32Connector(t32_api_path=T32_API_DLL_PATH)
    if not connector.t32_lib:
        pytest.fail("T32 API library failed to load in fixture.")
    connected = connector.connect(node="localhost", port="20000")
    if not connected:
        pytest.fail("Failed to connect to Trace32 in fixture.")
    yield connector
    print("\nTearing down T32 session...")
    connector.disconnect() 