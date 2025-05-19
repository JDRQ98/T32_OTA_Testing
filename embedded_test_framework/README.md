# Trace32 Remote Testing Framework

A Python-based framework for automating Trace32 testing via its Remote API.

## Prerequisites

- Windows 10/11
- Python 3.11 or later
- Trace32 installed with Remote API support
- Trace32 instance running with API enabled
- For remote execution:
  - Network connectivity between your machine and the test bench
  - Trace32 API DLL (`t32api64.dll` or `t32api.dll`) on your machine
  - Test bench's firewall allowing connections on the configured port

## Setup

1. **Clone the repository**
   ```powershell
   git clone <repository-url>
   cd embedded_test_framework
   ```

2. **Create and activate virtual environment**
   ```powershell
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install pytest
   ```

## Configuration

1. **Trace32 API DLL**
   - Ensure the Trace32 API DLL (`t32api64.dll` or `t32api.dll`) is either:
     - In your system PATH, or
     - Specify its path in `config/global_settings.ini`:
       ```ini
       [Trace32]
       api_dll_path = C:/T32/bin/windows64/t32api64.dll  # Adjust path as needed
       ```

2. **Trace32 Connection Settings**
   - Edit `config/global_settings.ini` to match your setup:
     ```ini
     [Trace32]
     # For local execution (Trace32 on same machine):
     node = localhost
     port = 20000

     # For remote execution (Trace32 on test bench):
     node = 192.168.1.100  # Replace with test bench IP
     port = 20000         # Must match port in Trace32 API command
     ```

3. **Enable Trace32 API on Test Bench**
   - Start Trace32 on the test bench
   - In Trace32 command line, type:
     ```
     API 20000  # Use the same port as in global_settings.ini
     ```
   - Verify API is enabled in Trace32 AREA window

## Remote Execution Setup

1. **On Your Development Machine**
   - Install Python and the framework
   - Copy the Trace32 API DLL to your machine
   - Configure `global_settings.ini` with test bench IP
   - Ensure network connectivity to test bench

2. **On the Test Bench**
   - Start Trace32
   - Enable API with correct port
   - Configure firewall to allow incoming connections:
     ```powershell
     # Open port in Windows Firewall (run as Administrator)
     New-NetFirewallRule -DisplayName "Trace32 API" -Direction Inbound -Protocol TCP -LocalPort 20000 -Action Allow
     ```

3. **Verify Connection**
   - Run a simple test to verify connectivity:
     ```powershell
     python run_tests.py tests/test_connection.py
     ```
   - Check Trace32 AREA window on test bench for connection messages

## Running Tests

1. **Ensure Trace32 is running with API enabled on test bench**
   - Verify Trace32 is running
   - Confirm API is enabled (check Trace32 AREA window for connection messages)

2. **Run all tests**
   ```powershell
   python run_tests.py
   ```

3. **Run specific tests**
   ```powershell
   # Run a specific test file
   python run_tests.py tests/test_connection.py

   # Run a specific test directory
   python run_tests.py tests/
   ```

## Project Structure

```
embedded_test_framework/
├── .venv/                  # Virtual environment
├── config/
│   └── global_settings.ini # Configuration file
├── cmm_scripts/
│   └── common/
│       └── hello.cmm      # Example CMM script
├── src/
│   └── test_framework/
│       ├── __init__.py
│       ├── t32_connector.py
│       └── config_loader.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_connection.py
│   └── test_cmm_execution.py
└── run_tests.py           # Test runner
```

## Troubleshooting

1. **DLL Loading Issues**
   - Error: "Could not load Trace32 API library"
   - Solution: Verify DLL path in `global_settings.ini` or ensure DLL is in system PATH

2. **Connection Issues**
   - Error: "T32_Attach failed"
   - Solution: 
     - Verify Trace32 is running on test bench
     - Confirm API is enabled (API command executed)
     - Check node/port in `global_settings.ini`
     - Verify network connectivity (try ping to test bench)
     - Check firewall settings on test bench

3. **Network Issues**
   - Error: Connection timeout
   - Solution:
     - Verify test bench IP is correct
     - Check firewall rules on test bench
     - Ensure no network restrictions between machines
     - Try telnet to test bench port to verify connectivity

4. **Test Failures**
   - If tests fail with "T32 session not connected":
     - Check Trace32 is running on test bench
     - Verify API is enabled
     - Confirm connection settings in `global_settings.ini`
     - Check network connectivity

## Notes

- The framework uses pytest for test execution
- Tests are session-scoped (one Trace32 connection per test run)
- CMM scripts should be placed in `cmm_scripts/` directory
- Always ensure Trace32 is running with API enabled before running tests
- For remote execution, ensure stable network connection
- Consider network latency when running tests remotely 