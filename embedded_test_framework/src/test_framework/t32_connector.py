import ctypes
import os

class T32Connector:
    def __init__(self, t32_api_path=None):
        self.t32_lib = None
        self.api_path = t32_api_path
        self._is_connected = False  # Add connection status flag
        self._load_t32_api()

    @property
    def is_connected(self):
        return self._is_connected

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

        # Define T32_Config prototype
        self.t32_lib.T32_Config.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.t32_lib.T32_Config.restype = None

        print(f"Configuring T32 connection: NODE={node}, PORT={port}, PACKLEN=1024")
        self.t32_lib.T32_Config(b"NODE=", node.encode('ascii'))
        self.t32_lib.T32_Config(b"PORT=", port.encode('ascii'))
        self.t32_lib.T32_Config(b"PACKLEN=", b"1024")

        # Define T32_Init prototype
        self.t32_lib.T32_Init.argtypes = []
        self.t32_lib.T32_Init.restype = ctypes.c_int

        print("Initializing T32 connection...")
        status = self.t32_lib.T32_Init()
        if status != 0:
            print(f"Error: T32_Init failed with status {status}")
            self._is_connected = False
            return False
        print("T32_Init successful.")

        # Define T32_Attach prototype
        self.t32_lib.T32_Attach.argtypes = [ctypes.c_int]
        self.t32_lib.T32_Attach.restype = ctypes.c_int

        print("Attaching to T32 API...")
        status = self.t32_lib.T32_Attach(1)  # T32_ATTACH_API = 1
        if status != 0:
            print(f"Error: T32_Attach failed with status {status}")
            self._is_connected = False
            return False
        print("T32_Attach successful. Connection established.")
        self._is_connected = True
        return True

    def disconnect(self):
        if not self.t32_lib:
            print("T32 API library not loaded. Nothing to disconnect.")
            return

        if not self._is_connected:
            print("Not connected to T32. Nothing to disconnect.")
            return

        # Define T32_Exit prototype
        self.t32_lib.T32_Exit.argtypes = []
        self.t32_lib.T32_Exit.restype = ctypes.c_int

        print("Disconnecting from T32...")
        status = self.t32_lib.T32_Exit()
        if status != 0:
            print(f"Warning: T32_Exit returned status {status}")
        else:
            print("T32_Exit successful.")
        self._is_connected = False

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
