import pytest
import sys
import argparse

if __name__ == "__main__":
    print("Starting test execution via run_tests.py...")
    parser = argparse.ArgumentParser(description="Run automated tests for embedded framework.")
    parser.add_argument(
        "test_path",
        nargs="*",
        default=["tests"],
        help="Path to test file or directory. Can specify multiple. Defaults to 'tests/'."
    )
    args = parser.parse_args()
    pytest_args = args.test_path
    print(f"Running pytest with arguments: {pytest_args}")
    exit_code = pytest.main(pytest_args)
    print(f"Test execution finished with exit code: {exit_code}")
    sys.exit(exit_code) 