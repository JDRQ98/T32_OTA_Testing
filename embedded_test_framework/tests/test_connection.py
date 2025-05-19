import pytest
from src.test_framework.t32_connector import T32Connector

# Hardcode T32 API path for now for the test, or ensure it's in system PATH
T32_API_DLL_PATH = None  # Let it try to find in PATH by default

def test_can_connect_and_disconnect():
    """Tests basic connection and disconnection to a T32 instance."""
    connector = T32Connector(t32_api_path=T32_API_DLL_PATH)
    assert connector.t32_lib is not None, "T32 API library failed to load"

    # For this test, Trace32 must be running and configured for API on localhost:20000
    # To make this test runnable, ensure T32 is manually started with API enabled.
    # e.g. t32marm -c myconfig.cfg API 20000
    
    connection_successful = connector.connect(node="localhost", port="20000")
    assert connection_successful, "Failed to connect to Trace32"
    assert connector.is_connected, "Connector state is not 'connected' after successful connect"

    connector.disconnect()
    assert not connector.is_connected, "Connector state is still 'connected' after disconnect"
