# Embedded Test Framework

A Python-based test automation framework for embedded systems using Trace32.

## Prerequisites

- Windows 10/11
- Python 3.11 or later
- Trace32 with Remote API support
- Network connectivity (for remote execution)
- Trace32 API DLL on your machine

## Setup

1. Clone the repository:
```powershell
git clone https://github.com/JDRQ98/T32_OTA_Testing
cd embedded_test_framework
```

2. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Configuration

### Local Execution
1. Set the Trace32 API DLL path in `config/global_settings.ini`:
```ini
[Trace32]
api_dll_path = C:\T32\bin\windows64\t32api64.dll
node = localhost
port = 20000
```

### Remote Execution
1. Set the test bench IP and port in `config/global_settings.ini`:
```ini
[Trace32]
api_dll_path = C:\T32\bin\windows64\t32api64.dll
node = 192.168.1.100  # Test bench IP
port = 20000
```

2. Ensure Trace32 is running on the test bench with API enabled:
   - Start Trace32
   - Enable Remote API in Trace32 settings
   - Verify the API port matches your configuration

## Usage Modes

### Graphical User Interface (GUI)
The framework includes a GUI for easy test execution and connection management:

1. **Launch the GUI**
   ```powershell
   python -m gui.main_window
   ```

2. **Connection Management**
   - Enter Trace32 node/IP and port
   - Configure retry settings
   - Check connection status
   - Test connection health

3. **Test Execution**
   - Select test files or directories
   - Configure test options
   - View real-time test output
   - Stop running tests

4. **Features**
   - Real-time connection status
   - Connection health checks
   - Test output display
   - Test execution controls
   - Settings persistence

### Interactive Development
When developing and debugging tests, you can use the framework interactively:

1. **Quick Connection Check**
   ```powershell
   # Verify connection before running tests
   python run_tests.py --check-connection
   ```

2. **Run Specific Tests**
   ```powershell
   # Run a single test file
   python run_tests.py tests/test_connection.py

   # Run tests with custom connection settings
   python run_tests.py --node 192.168.1.100 --port 20000 tests/test_connection.py
   ```

3. **Debug Mode**
   ```powershell
   # Run tests with pytest's debug options
   python run_tests.py -v --pdb tests/test_connection.py
   ```

### Headless Operation
For CI/CD pipelines and automated testing:

1. **Basic CI/CD Integration**
   ```yaml
   # Example GitHub Actions workflow
   name: Run Tests
   on: [push, pull_request]
   jobs:
     test:
       runs-on: windows-latest
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.11'
         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
         - name: Run tests
           run: |
             python run_tests.py --node ${{ secrets.T32_NODE }} --port ${{ secrets.T32_PORT }}
   ```

2. **Automated Test Execution**
   ```powershell
   # Run all tests with retry logic
   python run_tests.py --max-retries 3 --retry-delay 2.0

   # Run specific test suite with custom settings
   python run_tests.py --node 192.168.1.100 --port 20000 tests/suite_name/
   ```

3. **Scheduled Testing**
   ```powershell
   # Windows Task Scheduler command
   python run_tests.py --node 192.168.1.100 --port 20000 --max-retries 3
   ```

### Best Practices

#### For Developers
1. Always check connection before running tests:
   ```powershell
   python run_tests.py --check-connection
   ```

2. Use specific test paths during development:
   ```powershell
   python run_tests.py tests/your_test_file.py
   ```

3. Enable verbose output for debugging:
   ```powershell
   python run_tests.py -v tests/your_test_file.py
   ```

#### For CI/CD
1. Store sensitive information in environment variables:
   ```powershell
   $env:T32_NODE = "192.168.1.100"
   $env:T32_PORT = "20000"
   python run_tests.py
   ```

2. Use retry logic for stability:
   ```powershell
   python run_tests.py --max-retries 3 --retry-delay 2.0
   ```

3. Capture test results:
   ```powershell
   python run_tests.py --junitxml=test-results.xml
   ```

## Running Tests

### Basic Usage
1. Ensure Trace32 is running on the target machine
2. Run all tests:
```powershell
python run_tests.py
```

3. Run specific test files:
```powershell
python run_tests.py tests/test_connection.py
```

### Command Line Options
The framework supports several command-line arguments to override configuration settings:

```powershell
# Override connection parameters
python run_tests.py --node 192.168.1.100 --port 20000

# Configure retry behavior
python run_tests.py --max-retries 3 --retry-delay 2.0

# Check connection health without running tests
python run_tests.py --check-connection

# Combine options
python run_tests.py --node 192.168.1.100 --port 20000 --max-retries 3 --retry-delay 2.0 tests/test_connection.py
```

Available options:
- `--node`: Override Trace32 node/IP address
- `--port`: Override Trace32 API port
- `--max-retries`: Number of connection attempts (default: 1)
- `--retry-delay`: Delay in seconds between retries (default: 1.0)
- `--check-connection`: Only check connection health without running tests

### Connection Health Check
The `--check-connection` option allows you to verify your Trace32 connection settings before running tests. This is useful for:
- Troubleshooting connection issues
- Verifying network connectivity
- Testing configuration changes
- CI/CD pipeline setup

Example usage:
```powershell
# Check connection with default settings
python run_tests.py --check-connection

# Check connection with custom settings
python run_tests.py --check-connection --node 192.168.1.100 --port 20000 --max-retries 3
```

The health check will:
1. Load the Trace32 API DLL
2. Attempt to connect to Trace32
3. Execute a simple CMM command to verify the connection
4. Report success or failure

### Remote Execution Setup

#### On Development Machine
1. Install the framework and dependencies
2. Configure `global_settings.ini` with test bench IP
3. Ensure Trace32 API DLL is accessible
4. Run tests with appropriate connection parameters

#### On Test Bench
1. Install Trace32 with Remote API support
2. Configure Trace32 to accept remote connections
3. Open required ports in firewall
4. Start Trace32 before running tests

## Project Structure
```
embedded_test_framework/
├── config/
│   └── global_settings.ini
├── src/
│   └── test_framework/
│       ├── __init__.py
│       ├── t32_connector.py
│       └── config_loader.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_connection.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── connection_panel.py
│   └── test_panel.py
├── cmm_scripts/
│   └── common/
│       └── hello.cmm
├── requirements.txt
└── run_tests.py
```

## Troubleshooting

### DLL Loading Issues
- Verify the DLL path in `global_settings.ini`
- Ensure the DLL is in the system PATH
- Check DLL architecture matches Python (32/64 bit)

### Connection Issues
- Verify Trace32 is running on the target
- Check IP and port settings
- Ensure firewall allows the connection
- Verify network connectivity
- Use `--check-connection` to diagnose issues

### Network Issues
- Check if test bench is reachable (ping)
- Verify port is open (telnet)
- Check firewall settings on both machines
- Ensure Trace32 API is enabled on test bench

### GUI Issues
- Ensure Python and tkinter are properly installed
- Check if the GUI process has necessary permissions
- Verify all required dependencies are installed
- Check the console for any error messages

## Notes
- The framework requires the Trace32 API DLL to be accessible
- For remote execution, Trace32 must be running on the test bench
- Connection parameters can be overridden via command line
- The framework supports automatic retry on connection failure
- Use `--check-connection` to verify setup before running tests
- The GUI provides an alternative to command-line operation 