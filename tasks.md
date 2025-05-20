MVP Build Plan: CI/CD Test Automation Framework

Goal of MVP:

    Run a single Python test using pytest.

    The test connects to a manually pre-configured and running Trace32 instance.

    The test executes a simple "Hello World" CMM script via the Trace32 Remote API.

    Connection details (IP/port) are read from a basic INI configuration file.

    Tests are kicked off by a very simple Python script (run_tests.py).

    Output is via pytest console; no complex reports yet.

Phase 1: Basic Project Setup & Python-Trace32 Connection

Task 1.1: Project Directory and Virtual Environment Setup

    Start: No project directory exists.

    Action:

        Create the main project directory: embedded_test_framework/

        Navigate into embedded_test_framework/.

        Create a Python virtual environment (e.g., python -m venv .venv).

        Activate the virtual environment (e.g., source .venv/bin/activate or .venv\Scripts\activate).

        Create an empty requirements.txt file in the embedded_test_framework/ directory.

    End: Project directory embedded_test_framework/ with an activated virtual environment and an empty requirements.txt exists.

    Test:

        From within embedded_test_framework/ with the venv activated, run python --version. It should show the Python version from the virtual environment.

        Run pip freeze. It should be empty or show only core packages like pip and setuptools.

Task 1.2: Create src/test_framework Package Structure

    Start: embedded_test_framework/ exists with .venv/ and requirements.txt.

    Action:

        Inside embedded_test_framework/, create a directory named src/.

        Inside src/, create a directory named test_framework/.

        Inside src/test_framework/, create an empty file named __init__.py.

        Inside src/test_framework/, create an empty file named t32_connector.py.

    End: Basic package structure src/test_framework/ with __init__.py and an empty t32_connector.py exists.

    Test:

        Create a temporary Python script (e.g., check_import.py) in the embedded_test_framework/src/ directory with content:

              
        try:
            import test_framework
            print("Successfully imported test_framework")
        except ImportError as e:
            print(f"Failed to import test_framework: {e}")

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

        Run python check_import.py from the embedded_test_framework/src/ directory. It should print "Successfully imported test_framework". Delete check_import.py afterwards.

Task 1.3: Basic Trace32 API DLL/SO Loading in T32Connector (Stub)

    Start: t32_connector.py is empty. Assume Trace32 is installed and the path to t32api[64].dll (Windows) or t32api.so (Linux) is known.

    Action:

        Open src/test_framework/t32_connector.py.

        Add the following code:

              
        import ctypes
        import os

        class T32Connector:
            def __init__(self, t32_api_path=None):
                self.t32_lib = None
                self.api_path = t32_api_path
                self._load_t32_api()

            def _load_t32_api(self):
                if self.api_path:
                    # Try loading from the specified path
                    try:
                        self.t32_lib = ctypes.cdll.LoadLibrary(self.api_path)
                        print(f"Successfully loaded T32 API from: {self.api_path}")
                        return
                    except OSError as e:
                        print(f"Failed to load T32 API from {self.api_path}: {e}")
                        # Fall through to try system paths if specific path fails
                
                # Try common names if no path or specific path failed
                lib_names = []
                if os.name == 'nt': # Windows
                    lib_names = ['t32api64.dll', 't32api.dll']
                else: # Linux/macOS
                    lib_names = ['t32api.so']

                for lib_name in lib_names:
                    try:
                        self.t32_lib = ctypes.cdll.LoadLibrary(lib_name)
                        print(f"Successfully loaded T32 API: {lib_name}")
                        return
                    except OSError:
                        continue
                
                print("Error: Could not load Trace32 API library. Ensure it's in PATH or t32_api_path is correct.")
                # raise OSError("Could not load Trace32 API library.") # Consider raising an error

            def connect(self, node="localhost", port="20000"):
                if not self.t32_lib:
                    print("T32 API library not loaded. Cannot connect.")
                    return False
                print(f"Stub: Attempting to configure T32 connection to {node}:{port}")
                # Actual API calls will be added here
                print("Stub: Attempting to initialize T32 connection")
                print("Stub: Attempting to attach to T32 API")
                print("Connection attempt finished (stub).")
                return True # Placeholder

            def disconnect(self):
                if not self.t32_lib:
                    print("T32 API library not loaded. Nothing to disconnect.")
                    return
                print("Stub: Disconnecting from T32.")
                # Actual API call T32_Exit will be added here

            

        IGNORE_WHEN_COPYING_START

    Use code with caution. Python
    IGNORE_WHEN_COPYING_END

End: T32Connector class exists and attempts to load the Trace32 API library upon instantiation. It has stub connect and disconnect methods.

Test:

    Create a temporary script main_test_connector.py in the embedded_test_framework/ root directory:

          
    from src.test_framework.t32_connector import T32Connector

    # Option 1: Let it try to find the DLL/SO in system path
    # connector = T32Connector()

    # Option 2: Specify path if not in system PATH (MODIFY THIS PATH)
    # For Windows:
    # connector = T32Connector(t32_api_path="C:/T32/bin/windows64/t32api64.dll")
    # For Linux:
    # connector = T32Connector(t32_api_path="/opt/t32/bin/pc_linux64/t32api.so")

    # Choose one of the above instantiations
    connector = T32Connector() # Or with path

    if connector.t32_lib:
        print("T32Connector initialized with loaded library.")
        connector.connect()
        connector.disconnect()
    else:
        print("T32Connector failed to load library.")

        

    IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

        Run python main_test_connector.py.

        Verify output indicating success or failure of library loading, and the stub connection messages.

        Important: Adjust the t32_api_path in main_test_connector.py if the library isn't found automatically. This path will later come from configuration.

        Delete main_test_connector.py after testing.

Task 1.4: Implement T32_Config API Calls in connect Method

    Start: T32Connector can load the API library; connect method is a stub.

    Action:

        Modify src/test_framework/t32_connector.py:

              
        # ... (imports and __init__, _load_t32_api as before) ...
            def connect(self, node="localhost", port="20000"):
                if not self.t32_lib:
                    print("T32 API library not loaded. Cannot connect.")
                    return False

                # Define T32_Config prototype
                # T32_Config(char *name, char *value)
                self.t32_lib.T32_Config.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
                self.t32_lib.T32_Config.restype = None # It's void

                print(f"Configuring T32 connection: NODE={node}, PORT={port}, PACKLEN=1024")
                self.t32_lib.T32_Config(b"NODE=", node.encode('ascii'))
                self.t32_lib.T32_Config(b"PORT=", port.encode('ascii'))
                self.t32_lib.T32_Config(b"PACKLEN=", b"1024") # Default, can be configured later

                print("Stub: Attempting to initialize T32 connection") # Keep stubs for next steps
                print("Stub: Attempting to attach to T32 API")
                print("Configuration set.")
                return True # Placeholder
        # ... (disconnect as before) ...

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: connect method now calls T32_Config with provided or default values.

    Test:

        Use a similar main_test_connector.py as in Task 1.3.

        Run python main_test_connector.py.

        Verify the print output showing "Configuring T32 connection..." and "Configuration set."

        No external Trace32 instance is needed yet. The test ensures API calls don't crash due to incorrect signatures.

Task 1.5: Implement T32_Init API Call in connect Method

    Start: connect method calls T32_Config.

    Action:

        Modify src/test_framework/t32_connector.py:

              
        # ... (imports and __init__, _load_t32_api as before) ...
            def connect(self, node="localhost", port="20000"):
                # ... (T32_Config setup and calls as before) ...

                # Define T32_Init prototype
                # T32_Init(void)
                self.t32_lib.T32_Init.argtypes = []
                self.t32_lib.T32_Init.restype = ctypes.c_int # Returns status

                print("Initializing T32 connection...")
                status = self.t32_lib.T32_Init()
                if status != 0:
                    print(f"Error: T32_Init failed with status {status}")
                    return False
                print("T32_Init successful.")

                print("Stub: Attempting to attach to T32 API") # Keep stub for next step
                return True # Placeholder
        # ... (disconnect as before) ...

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: connect method now also calls T32_Init and checks its status.

    Test:

        Use main_test_connector.py.

        Run python main_test_connector.py.

        Output should show "T32_Init successful." or an error if T32_Init fails (e.g., if Trace32 is not running on the specified node/port, this call might still succeed locally before T32_Attach makes the actual connection attempt, behavior can vary slightly with T32 versions).

Task 1.6: Implement T32_Attach API Call in connect Method & is_connected Property

    Start: connect method calls T32_Init.

    Action:

        Modify src/test_framework/t32_connector.py:

              
        # ... (imports and __init__, _load_t32_api as before) ...
        class T32Connector:
            def __init__(self, t32_api_path=None):
                # ... (as before) ...
                self._is_connected = False # Add connection status flag

            # ... (_load_t32_api as before) ...

            @property
            def is_connected(self):
                return self._is_connected

            def connect(self, node="localhost", port="20000"):
                # ... (T32_Config and T32_Init calls as before) ...
                # Ensure T32_Init was successful before proceeding
                # (The previous step already has this logic, just ensure it's there)
                # if not self.t32_lib.T32_Init() == 0: return False 

                # Define T32_Attach prototype
                # T32_Attach(int mode) - mode 1 for T32_ATTACH_API
                self.t32_lib.T32_Attach.argtypes = [ctypes.c_int]
                self.t32_lib.T32_Attach.restype = ctypes.c_int # Returns status

                print("Attaching to T32 API...")
                # T32_ATTACH_NORMAL = 0, T32_ATTACH_API = 1
                status = self.t32_lib.T32_Attach(1) 
                if status != 0:
                    print(f"Error: T32_Attach failed with status {status}")
                    # Potentially call T32_Exit if Init succeeded but Attach failed
                    # self.t32_lib.T32_Exit() # Define T32_Exit prototype if used here
                    self._is_connected = False
                    return False
                
                print("T32_Attach successful. Connection established.")
                self._is_connected = True
                return True
        # ... (disconnect will be modified in next step) ...

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: connect method calls T32_Attach, updates _is_connected flag. is_connected property added.

    Test:

        Crucial: Manually start a Trace32 instance. Configure it for remote API access on localhost:20000 (or the defaults in connect).

            Example: t32marm -c myconfig.cfg API 20000 (replace t32marm with your CPU type, e.g., t32mppc).

            Or, in an already running T32, type API 20000 in the command line.

        Use main_test_connector.py and ensure it calls connect() and prints connector.is_connected.

        Run python main_test_connector.py.

        Verify "T32_Attach successful. Connection established." is printed and connector.is_connected returns True. Check Trace32 AREA window for connection messages.

        Stop the Trace32 instance and re-run. Verify T32_Attach fails and is_connected is False.

Task 1.7: Implement T32_Exit API Call in disconnect Method

    Start: connect method can establish a connection; _is_connected flag exists.

    Action:

        Modify src/test_framework/t32_connector.py:

              
        # ... (imports, __init__, _load_t32_api, is_connected, connect as before) ...
            def disconnect(self):
                if not self.t32_lib:
                    print("T32 API library not loaded. Nothing to disconnect.")
                    return

                if not self._is_connected:
                    print("Not connected to T32. Nothing to disconnect.")
                    # Even if not "attached", if T32_Init was called, T32_Exit might be needed
                    # However, for simplicity, we only call T32_Exit if fully connected.
                    # A more robust implementation might track T32_Init state separately.
                    return

                # Define T32_Exit prototype
                # T32_Exit(void)
                self.t32_lib.T32_Exit.argtypes = []
                self.t32_lib.T32_Exit.restype = ctypes.c_int # Returns status (usually 0)

                print("Disconnecting from T32...")
                status = self.t32_lib.T32_Exit()
                if status != 0:
                    print(f"Warning: T32_Exit returned status {status}")
                else:
                    print("T32_Exit successful.")
                self._is_connected = False

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: disconnect method calls T32_Exit if connected and updates _is_connected.

    Test:

        Manually start Trace32 with API enabled.

        Use main_test_connector.py to call connector.connect(...), print connector.is_connected, then connector.disconnect(), then print connector.is_connected again.

        Run python main_test_connector.py.

        Verify connection, is_connected becomes True, then disconnection messages, and is_connected becomes False.

Phase 2: Basic Test Structure with Pytest

Task 2.1: Install Pytest and Create Basic Test Directory Structure

    Start: Project has src/test_framework and a working T32Connector.

    Action:

        Add pytest to embedded_test_framework/requirements.txt:

              
        pytest

            

        IGNORE_WHEN_COPYING_START

        Use code with caution.
        IGNORE_WHEN_COPYING_END

        From embedded_test_framework/ with venv activated, run pip install -r requirements.txt.

        Create tests/ directory in the embedded_test_framework/ root.

        Inside tests/, create an empty file named __init__.py.

        Inside tests/, create an empty file named test_connection.py.

    End: pytest is installed. tests/ directory structure with test_connection.py exists.

    Test:

        From embedded_test_framework/ root, run pytest.

        It should report that it collected 0 items or 1 empty test file, and no tests ran.

Task 2.2: Write a Simple Pytest Test for T32 Connection

    Start: test_connection.py is empty. T32Connector works.

    Action:

        Edit tests/test_connection.py:

              
        import pytest
        from src.test_framework.t32_connector import T32Connector # Ensure PYTHONPATH allows this or adjust for editable install later

        # Hardcode T32 API path for now for the test, or ensure it's in system PATH
        # This will be improved with configuration later.
        # T32_API_DLL_PATH = "C:/T32/bin/windows64/t32api64.dll" # EXAMPLE -  MODIFY IF NEEDED
        T32_API_DLL_PATH = None # Let it try to find in PATH by default

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

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

        Note on PYTHONPATH for src imports: For pytest to find src.test_framework, you might need to:

            Run pytest from embedded_test_framework/.

            Or, later, make test_framework an installable package (e.g., pip install -e .). For MVP, running from root is fine.

    End: A pytest test test_can_connect_and_disconnect exists.

    Test:

        Manually start Trace32 with API enabled on localhost:20000.

        If you needed to set T32_API_DLL_PATH in Task 1.3, set it also in test_connection.py.

        From embedded_test_framework/ root, run pytest tests/test_connection.py.

        The test should pass. If it fails on import, ensure your PYTHONPATH is set up correctly or you are running pytest from the project root.

Task 2.3: Create conftest.py and a Basic t32_session Fixture

    Start: test_connection.py directly instantiates T32Connector.

    Action:

        Create tests/conftest.py in the embedded_test_framework/tests/ directory:

              
        import pytest
        from src.test_framework.t32_connector import T32Connector

        # Hardcode T32 API path for now for the fixture, or ensure it's in system PATH
        # This will be improved with configuration later.
        # T32_API_DLL_PATH = "C:/T32/bin/windows64/t32api64.dll" # EXAMPLE - MODIFY IF NEEDED
        T32_API_DLL_PATH = None # Let it try to find in PATH by default

        @pytest.fixture(scope="session")
        def t32_session():
            """Session-scoped fixture to manage T32 connection."""
            print("\nSetting up T32 session...")
            connector = T32Connector(t32_api_path=T32_API_DLL_PATH)
            if not connector.t32_lib:
                pytest.fail("T32 API library failed to load in fixture.")

            # For tests using this fixture, Trace32 must be running on localhost:20000
            connected = connector.connect(node="localhost", port="20000")
            if not connected:
                pytest.fail("Failed to connect to Trace32 in fixture.")
            
            yield connector  # Provide the connected connector to the test

            print("\nTearing down T32 session...")
            connector.disconnect()

            

        IGNORE_WHEN_COPYING_START

Use code with caution. Python
IGNORE_WHEN_COPYING_END

Modify tests/test_connection.py to use the fixture:

      
import pytest
# from src.test_framework.t32_connector import T32Connector # No longer needed here

def test_t32_fixture_connection(t32_session): # Use the fixture
    """Tests that the t32_session fixture provides a connected session."""
    assert t32_session is not None, "t32_session fixture is None"
    assert t32_session.is_connected, "t32_session fixture is not connected"
    print("T32 session is connected via fixture.")

    

IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: conftest.py provides a session-scoped t32_session fixture. The test uses this fixture.

    Test:

        Manually start Trace32 with API enabled on localhost:20000.

        If you needed to set T32_API_DLL_PATH, set it in conftest.py.

        From embedded_test_framework/ root, run pytest tests/test_connection.py -s (the -s shows print statements from fixture).

        The test should pass. Observe setup/teardown messages from the fixture.

Phase 3: Configuration Management

Task 3.1: Create config Directory and a Basic global_settings.ini

    Start: Project structure exists. Connection details are hardcoded in conftest.py.

    Action:

        Create config/ directory in the embedded_test_framework/ root.

        Inside config/, create global_settings.ini with the following content:

              
        [Trace32]
        node = localhost
        port = 20000
        # Optional: Add api_dll_path if needed, leave commented out or empty if relying on PATH
        # api_dll_path = C:/T32/bin/windows64/t32api64.dll
        api_dll_path =

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Ini
        IGNORE_WHEN_COPYING_END

        Ensure configparser is available (standard in Python 3.2+). If using older Python, add to requirements.txt and install.

    End: config/global_settings.ini file exists with T32 connection details.

    Test: Manually verify the file config/global_settings.ini exists and its content is correct.

Task 3.2: Create Basic config_loader.py

    Start: global_settings.ini exists.

    Action:

        Create src/test_framework/config_loader.py:

              
        import configparser
        import os

        def load_config(config_file_name="global_settings.ini"):
            """Loads configuration from an INI file."""
            # Assume config dir is one level up from src/test_framework/ and then into config/
            # Or, more robustly, determine project root. For MVP, relative path is okay.
            
            # Construct path relative to this file's directory (src/test_framework)
            # ../../config/global_settings.ini
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir_path = os.path.join(current_dir, "..", "..", "config")
            config_file_path = os.path.join(config_dir_path, config_file_name)

            if not os.path.exists(config_file_path):
                raise FileNotFoundError(f"Config file not found: {config_file_path}")

            parser = configparser.ConfigParser()
            parser.read(config_file_path)
            return parser

            

        IGNORE_WHEN_COPYING_START

    Use code with caution. Python
    IGNORE_WHEN_COPYING_END

End: config_loader.py can load settings from the INI file.

Test:

    Create a temporary script test_load_conf.py in embedded_test_framework/ root:

          
    from src.test_framework.config_loader import load_config

    try:
        config = load_config()
        print(f"Node: {config['Trace32']['node']}")
        print(f"Port: {config['Trace32']['port']}")
        api_path = config.get('Trace32', 'api_dll_path', fallback=None)
        if api_path: # Only print if it's not empty
             print(f"API DLL Path: {api_path}")
        else:
            print("API DLL Path: Not specified, relying on system PATH.")

    except Exception as e:
        print(f"Error loading config: {e}")

        

    IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

        Run python test_load_conf.py. It should print values from config/global_settings.ini.

        Delete test_load_conf.py.

Task 3.3: Use Loaded Configuration in t32_session Fixture

    Start: t32_session fixture has hardcoded connection details. config_loader.py exists.

    Action:

        Modify tests/conftest.py:

              
        import pytest
        from src.test_framework.t32_connector import T32Connector
        from src.test_framework.config_loader import load_config # Import the loader

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

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: t32_session fixture uses connection details from global_settings.ini.

    Test:

        Manually start Trace32 with API enabled (e.g., API 20000).

        Run pytest tests/test_connection.py -s. It should pass using settings from global_settings.ini.

        Modify config/global_settings.ini to use a different port (e.g., port = 20001).

        Run pytest tests/test_connection.py -s. It should fail to connect (because T32 is on 20000).

        Change Trace32 API port to 20001 (e.g., API 20001 in T32 cmd line) and re-run pytest. It should pass.

        Revert global_settings.ini port to 20000 and T32 API port to 20000.

Phase 4: CMM Script Execution

Task 4.1: Create cmm_scripts Directory and a Simple "Hello" CMM Script

    Start: Project structure exists.

    Action:

        Create cmm_scripts/ directory in the embedded_test_framework/ root.

        Inside cmm_scripts/, create common/ directory.

        Inside cmm_scripts/common/, create hello.cmm with the following content:

              
        ; Simple CMM script for testing
        PRINT "Hello from hello.cmm script!"
        ENDDO

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Cmm
        IGNORE_WHEN_COPYING_END

    End: A simple CMM script cmm_scripts/common/hello.cmm exists.

    Test: Manually verify the file cmm_scripts/common/hello.cmm exists and its content is correct.

Task 4.2: Implement T32_ExecuteScript API Call in T32Connector

    Start: T32Connector can connect/disconnect.

    Action:

        Modify src/test_framework/t32_connector.py:

              
        # ... (imports, __init__, _load_t32_api, is_connected, connect, disconnect as before) ...
        # Add this method to the T32Connector class:

            def run_cmm_script(self, script_path: str, args: list = None) -> int:
                """
                Executes a CMM script.
                :param script_path: Absolute or relative path to the .cmm script.
                                    T32 resolves relative paths based on its own CWD or settings.
                                    It's often best to provide absolute paths from Python.
                :param args: A list of string arguments for the script.
                :return: Status code from T32_ExecuteScript (0 for success).
                """
                if not self.is_connected:
                    print("Error: Not connected to Trace32. Cannot execute script.")
                    return -1 # Or raise an exception

                # T32_ExecuteScript(const char *pszPathName, const char *pszArgs[])
                self.t32_lib.T32_ExecuteScript.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
                self.t32_lib.T32_ExecuteScript.restype = ctypes.c_int

                script_path_bytes = script_path.encode('ascii')
                
                c_args = None
                if args:
                    # Convert Python list of strings to C-style array of char pointers
                    c_args_arr = (ctypes.c_char_p * (len(args) + 1))() # +1 for NULL terminator
                    for i, arg in enumerate(args):
                        c_args_arr[i] = arg.encode('ascii')
                    c_args_arr[len(args)] = None # Null-terminate the array
                    c_args = c_args_arr
                
                print(f"Executing CMM script: {script_path} with args: {args}")
                status = self.t32_lib.T32_ExecuteScript(script_path_bytes, c_args)
                
                if status != 0:
                    print(f"Error: T32_ExecuteScript for '{script_path}' failed with status {status}")
                else:
                    print(f"T32_ExecuteScript for '{script_path}' successful.")
                return status

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: T32Connector has a run_cmm_script method that can call T32_ExecuteScript.

    Test: This is primarily a code addition. It will be fully tested in the next task by actually calling it.

Task 4.3: Create a Pytest Test to Run the "Hello" CMM Script

    Start: hello.cmm exists. run_cmm_script method exists in T32Connector.

    Action:

        Create tests/test_cmm_execution.py in embedded_test_framework/tests/:

              
        import pytest
        import os

        def test_run_hello_cmm(t32_session): # Uses the existing t32_session fixture
            """Tests executing a simple CMM script."""
            assert t32_session.is_connected, "T32 session not connected at start of CMM test"

            # Construct an absolute path to the CMM script
            # Assumes tests are run from project root or paths are handled correctly
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            script_path = os.path.join(project_root, "cmm_scripts", "common", "hello.cmm")
            
            assert os.path.exists(script_path), f"CMM script not found at: {script_path}"

            print(f"Attempting to run CMM script: {script_path}")
            status = t32_session.run_cmm_script(script_path)
            
            # T32_ExecuteScript returns 0 on success for starting the script.
            # It doesn't wait for script completion or report script's internal errors directly.
            assert status == 0, f"run_cmm_script returned non-zero status: {status}"
            print("CMM script execution initiated successfully.")
            # For MVP, we manually check T32 AREA. Later, T32_GetMessage or other checks can be added.

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: A pytest test test_run_hello_cmm exists that attempts to run hello.cmm.

    Test:

        Manually start Trace32 with API enabled.

        From embedded_test_framework/ root, run pytest tests/test_cmm_execution.py -s.

        The test should pass (i.e., status == 0).

        Manually verify: The Trace32 AREA window should display "Hello from hello.cmm script!".

Phase 5: Basic Test Orchestration (Simple Runner)

Task 5.1: Create Basic run_tests.py CLI Entry Point

    Start: Pytest tests can be run using the pytest command directly.

    Action:

        Create run_tests.py in the embedded_test_framework/ root:

              
        import pytest
        import sys
        import os

        if __name__ == "__main__":
            print("Starting test execution via run_tests.py...")
            
            # Optional: Add src to PYTHONPATH if tests are run via `python run_tests.py`
            # and src is not installed as a package.
            # This ensures 'from src.test_framework...' imports work.
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # sys.path.insert(0, current_dir) # Add project root to allow `from src...`

            # Pytest will discover tests in the 'tests' directory by default
            # or any other paths passed as arguments.
            exit_code = pytest.main() # Runs all tests discovered by pytest default behavior
            
            print(f"Test execution finished with exit code: {exit_code}")
            sys.exit(exit_code)

            

        IGNORE_WHEN_COPYING_START

        Use code with caution. Python
        IGNORE_WHEN_COPYING_END

    End: run_tests.py script exists that can invoke pytest.main().

    Test:

        Manually start Trace32 with API enabled.

        From embedded_test_framework/ root, run python run_tests.py.

        It should discover and run all tests (test_connection.py::test_t32_fixture_connection and test_cmm_execution.py::test_run_hello_cmm).

        Verify console output shows tests running and their results.

Task 5.2: Add Simple Argument Parsing to run_tests.py (e.g., select test file/directory)

    Start: run_tests.py runs all discovered tests.

    Action:

        Modify run_tests.py in the embedded_test_framework/ root:

              
        import pytest
        import sys
        import argparse # Import argparse
        import os

        if __name__ == "__main__":
            print("Starting test execution via run_tests.py...")
            
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # sys.path.insert(0, current_dir)

            parser = argparse.ArgumentParser(description="Run automated tests for embedded framework.")
            parser.add_argument(
                "test_path", 
                nargs="*",  # 0 or more arguments
                default=["tests"], # Default to 'tests' directory if no path is given
                help="Path to test file or directory. Can specify multiple. Defaults to 'tests/'."
            )
            # Add other pytest arguments you want to expose, e.g., -k, -m, --html
            # For MVP, just the test path.
            # Example: parser.add_argument("-k", "--keyword", help="Pytest keyword expression")

            # Parse only known arguments for this script, pass others to pytest
            # For simplicity in MVP, we'll pass all given paths directly to pytest.
            # A more advanced setup would separate script args from pytest args.
            args = parser.parse_args()
            
            pytest_args = args.test_path
            # if args.keyword:
            #    pytest_args.extend(["-k", args.keyword])

            print(f"Running pytest with arguments: {pytest_args}")
            exit_code = pytest.main(pytest_args)
            
            print(f"Test execution finished with exit code: {exit_code}")
            sys.exit(exit_code)

            

        IGNORE_WHEN_COPYING_START

    Use code with caution. Python
    IGNORE_WHEN_COPYING_END

End: run_tests.py can accept one or more paths to run specific tests or test directories.

Test:

    Manually start Trace32 with API enabled.

    From embedded_test_framework/ root, try the following commands:

        python run_tests.py tests/test_connection.py (should run only connection test).

        python run_tests.py tests/test_cmm_execution.py (should run only CMM execution test).

        python run_tests.py tests (should run all tests in tests/ directory).

        python run_tests.py (should run all tests in tests/ directory due to default).

        python run_tests.py tests/test_connection.py tests/test_cmm_execution.py (should run both).

    Verify the correct tests are run based on the arguments.


Phase 6: Robust Connection Management & Usability Foundations
Task 6.1: Add Connection Retry Logic to T32Connector
Goal:
Improve reliability by automatically retrying Trace32 connections a configurable number of times with delays.
Action:
Add max_retries and retry_delay parameters to T32Connector.connect().
On connection failure, retry up to max_retries times, waiting retry_delay seconds between attempts.
Log each attempt and final failure.
Test:
Simulate a failed connection (wrong port/IP) and verify retries and error messages.
Simulate a delayed Trace32 startup and verify that a retry eventually succeeds.
Task 6.2: Expose Connection Parameters via CLI
Goal:
Allow users (and CI/CD) to override connection parameters (IP, port, retries) from the command line.
Action:
Update run_tests.py to accept --node, --port, --max-retries, and --retry-delay arguments.
These override values in global_settings.ini.
Pass these values to the test fixture and T32Connector.
Test:
Run tests with CLI overrides and verify the correct parameters are used.
Check that missing/invalid arguments are handled gracefully.
Task 6.3: Add Connection Health Check Command
Goal:
Provide a simple CLI command to check if Trace32 is reachable (for both users and CI/CD).
Action:
Add a --check-connection flag to run_tests.py.
When used, attempt to connect and disconnect, printing success/failure and exit code.
No tests are run in this mode.
Test:
Run with --check-connection to a valid and invalid Trace32 instance and verify output and exit code.
Task 6.4: Document Headless and Interactive Use
Goal:
Make it clear how to use the framework in both manual and CI/CD scenarios.
Action:
Update README.md with:
Example headless (CI/CD) usage, including connection retries and health checks.
Note on future GUI plans for interactive use.
Test:
Manual review of documentation for clarity and completeness.
Task 6.5: GUI Planning and Initial Implementation

    Start: Framework has robust connection management and CLI interface.

    Action:
        1. Create a new directory for GUI components:
           ```
           embedded_test_framework/
           └── gui/
               ├── __init__.py
               ├── main_window.py
               ├── connection_panel.py
               └── test_panel.py
           ```

        2. Define GUI requirements:
           - Connection management panel:
             * IP/Port input fields
             * Connection status indicator
             * Connect/Disconnect buttons
             * Retry settings
           - Test execution panel:
             * Test file/directory selection
             * Test execution controls
             * Test output display
             * Test results summary
           - Settings panel:
             * DLL path configuration
             * Default connection settings
             * Logging options

        3. Create basic GUI structure using tkinter:
           - Main window with menu bar
           - Tabbed interface for different panels
           - Status bar for connection and test status
           - Configuration persistence

        4. Implement connection panel:
           - Input validation
           - Real-time connection status
           - Error handling and user feedback
           - Connection history

        5. Add test execution features:
           - Test file browser
           - Test execution controls
           - Real-time test output
           - Test result visualization

    End: Basic GUI structure with connection management and test execution capabilities.

    Test:
        1. Launch GUI and verify all panels load correctly
        2. Test connection management:
           - Enter valid/invalid connection details
           - Verify connection status updates
           - Test retry functionality
        3. Test test execution:
           - Select and run individual tests
           - View test output
           - Verify test results display
        4. Test settings persistence:
           - Save and load configuration
           - Verify settings are maintained between sessions

    Dependencies:
        - Python 3.11 or later
        - tkinter (included in Python standard library)
        - Existing framework components

    Notes:
        - GUI should be optional (CLI remains primary interface)
        - Focus on usability and error handling
        - Consider future extensibility
        - Maintain separation of concerns between GUI and core functionality