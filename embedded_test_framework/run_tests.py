import pytest
import sys
import argparse
import os
from src.test_framework.t32_connector import T32Connector
from src.test_framework.config_loader import load_config

def check_connection(node, port, max_retries, retry_delay):
    """Check Trace32 connection health."""
    print("Checking Trace32 connection health...")
    
    # Load config for DLL path
    cfg = load_config("global_settings.ini")
    api_dll_path_cfg = cfg.get('Trace32', 'api_dll_path', fallback=None)
    t32_api_path = api_dll_path_cfg if api_dll_path_cfg and api_dll_path_cfg.strip() else None
    
    connector = T32Connector(t32_api_path=t32_api_path)
    if not connector.t32_lib:
        print("Error: Failed to load Trace32 API library.")
        return 1
        
    if not connector.connect(node=node, port=port, max_retries=max_retries, retry_delay=retry_delay):
        print("Error: Failed to connect to Trace32.")
        return 1
        
    if not connector.check_connection():
        print("Error: Connection health check failed.")
        connector.disconnect()
        return 1
        
    print("Connection health check passed successfully!")
    connector.disconnect()
    return 0

if __name__ == "__main__":
    print("Starting test execution via run_tests.py...")
    
    # Load configuration first
    cfg = load_config("global_settings.ini")
    
    parser = argparse.ArgumentParser(description="Run automated tests for embedded framework.")
    parser.add_argument(
        "test_path",
        nargs="*",
        default=["tests"],
        help="Path to test file or directory. Can specify multiple. Defaults to 'tests/'."
    )
    # Add connection parameter overrides
    parser.add_argument(
        "--node",
        help="Override Trace32 node/IP from config file"
    )
    parser.add_argument(
        "--port",
        help="Override Trace32 port from config file"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        help="Override max connection retries from config file"
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        help="Override retry delay (seconds) from config file"
    )
    parser.add_argument(
        "--check-connection",
        action="store_true",
        help="Only check connection health without running tests"
    )

    args = parser.parse_args()
    
    # Set environment variables for connection parameters if provided
    if args.node:
        os.environ["T32_NODE"] = args.node
    if args.port:
        os.environ["T32_PORT"] = args.port
    if args.max_retries is not None:
        os.environ["T32_MAX_RETRIES"] = str(args.max_retries)
    if args.retry_delay is not None:
        os.environ["T32_RETRY_DELAY"] = str(args.retry_delay)

    # Get connection parameters with proper priority:
    # 1. Command line arguments
    # 2. Environment variables
    # 3. Configuration file
    node = args.node or os.environ.get("T32_NODE") or cfg.get('Trace32', 'node')
    port = args.port or os.environ.get("T32_PORT") or cfg.get('Trace32', 'port')
    max_retries = args.max_retries or int(os.environ.get("T32_MAX_RETRIES", "1"))
    retry_delay = args.retry_delay or float(os.environ.get("T32_RETRY_DELAY", "1.0"))

    if args.check_connection:
        exit_code = check_connection(node, port, max_retries, retry_delay)
        sys.exit(exit_code)

    pytest_args = args.test_path
    print(f"Running pytest with arguments: {pytest_args}")
    exit_code = pytest.main(pytest_args)
    
    print(f"Test execution finished with exit code: {exit_code}")
    sys.exit(exit_code) 