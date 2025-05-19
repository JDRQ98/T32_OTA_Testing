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