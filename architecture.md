      
# CI/CD Test Automation Framework for Embedded Systems (Trace32 & Python)

## 1. Overview

This architecture describes a Python-based framework for automating tests on embedded targets using the Trace32 Remote API. It allows tests to be defined in Python, leveraging `.cmm` scripts for low-level target interaction, and can be triggered manually or by a CI/CD pipeline.

```mermaid
graph TD
    subgraph "CI/CD System (e.g., Jenkins, GitLab CI)"
        A[Pipeline Definition] --> B{Trigger}
    end

    subgraph "User Environment"
        C[User CLI] --> B
    end

    B --> D[Python Test Orchestrator]

    subgraph "Test Framework Core"
        D -- Loads --> E[Configuration Files (.ini/.yaml)]
        D -- Discovers & Executes --> F[Python Test Suites (pytest)]
        F -- Uses --> G[Trace32 Python API Wrapper]
        G -- Executes --> H[.cmm Scripts]
        G -- Communicates via Remote API (TCP/IP over VPN) --> I[Trace32 Instance]
    end

    I -- JTAG/SWD etc. --> J[Embedded Target Hardware]

    D -- Generates --> K[Test Reports (JUnit XML, HTML)]
    D -- Generates --> L[Logs]

    K -- Uploaded to --> A
    L -- Uploaded to --> A

    classDef ciSystem fill:#D6EAF8,stroke:#3498DB
    class A,B ciSystem

    classDef userEnv fill:#D5F5E3,stroke:#2ECC71
    class C userEnv

    classDef frameworkCore fill:#FCF3CF,stroke:#F1C40F
    class D,E,F,G,H,K,L frameworkCore

    classDef t32 fill:#EBDEF0,stroke:#8E44AD
    class I t32

    classDef target fill:#FDEDEC,stroke:#E74C3C
    class J target

    

IGNORE_WHEN_COPYING_START
Use code with caution. Markdown
IGNORE_WHEN_COPYING_END
2. File and Folder Structure

      
embedded_test_framework/
├── .venv/                     # Python virtual environment
├── src/
│   └── test_framework/        # Core framework library (installable package)
│       ├── __init__.py
│       ├── t32_connector.py   # Python wrapper for Trace32 Remote API
│       ├── config_loader.py   # Handles loading of various configs
│       ├── reporting.py       # Utilities for report generation
│       └── utils.py           # Common utility functions
├── tests/                     # Test suites and individual test cases
│   ├── conftest.py            # Pytest fixtures (e.g., t32_session)
│   ├── common/                # Common test steps or shared test logic
│   │   └── __init__.py
│   │   └── setup_teardown.py
│   ├── suite_smoke/
│   │   ├── __init__.py
│   │   └── test_boot.py
│   │   └── test_peripheral_x.py
│   └── suite_regression/
│       ├── __init__.py
│       └── test_memory_rw.py
│       └── test_algorithm_y.py
├── cmm_scripts/               # Trace32 CMM scripts
│   ├── common/                # General purpose CMM scripts
│   │   ├── connect_target.cmm
│   │   ├── load_elf.cmm
│   │   ├── reset_target.cmm
│   │   └── read_mem.cmm
│   ├── specific_helpers/      # CMMs for specific complex test steps
│   │   └── init_complex_peripheral.cmm
├── config/                    # Configuration files
│   ├── global_settings.ini    # Global framework settings (T32 paths, logging levels)
│   ├── targets/               # Target-specific configurations
│   │   ├── target_A.ini       # Config for Target A (e.g., ELF path, T32 IP)
│   │   └── target_B.ini       # Config for Target B
│   └── test_suites/           # (Optional) Configurations for specific test suites
│       └── smoke_suite_config.ini
├── reports/                   # Output directory for test reports (gitignored)
├── logs/                      # Output directory for logs (gitignored)
├── run_tests.py               # Main CLI entry point for running tests
├── requirements.txt           # Python package dependencies (pytest, t32api, etc.)
├── pytest.ini                 # Pytest configuration
└── README.md                  # Project documentation

    

IGNORE_WHEN_COPYING_START
Use code with caution.
IGNORE_WHEN_COPYING_END
3. What Each Part Does

    .venv/: Houses the Python interpreter and installed packages for this project, ensuring dependency isolation.

    src/test_framework/: This is the core Python library of your test framework.

        t32_connector.py:

            Manages the connection to the Trace32 instance via its remote API (e.g., ctypes binding to t32api.dll or t32api.so).

            Provides Python methods to send commands, execute CMM scripts, read/write memory, check register values, handle breakpoints, etc.

            Abstracts away the low-level details of the Trace32 API.

            Handles API initialization, connection, disconnection, and error handling.

        config_loader.py:

            Loads configuration from .ini or .yaml files.

            Merges global, target-specific, and potentially suite-specific configurations.

            Provides an easy way to access configuration values throughout the framework.

        reporting.py: Helper functions for generating or formatting test reports beyond what pytest provides by default, if needed.

        utils.py: General utility functions (e.g., custom logging setup, file helpers, string manipulation) used across the framework.

    tests/: Contains the actual test logic written in Python, using a test runner like pytest.

        conftest.py: Defines pytest fixtures. A key fixture here would be t32_session, which initializes t32_connector for a test or session, loads target configuration, and handles cleanup.

        common/: Reusable Python test functions or classes that represent common test sequences or verifications.

        suite_*/test_*.py: Python files containing test cases. Each function (e.g., test_boot_sequence) would:

            Use the t32_session fixture.

            Call methods on t32_connector to interact with the target (e.g., t32.run_cmm_script("load_elf.cmm", elf_path=...), t32.read_memory(...), t32.set_breakpoint(...)).

            Use pytest assertions (assert) to verify outcomes.

    cmm_scripts/: Directory for Trace32 CMM (.cmm) scripts.

        common/: Generic CMM scripts for fundamental operations (e.g., connecting, loading code, resetting, basic memory reads). These are often parameterized and called from Python.

        specific_helpers/: More complex or test-specific CMM scripts that might be easier to write in CMM than orchestrate via many individual API calls from Python.

    config/:

        global_settings.ini: Settings like default Trace32 installation path (if needed to find API DLLs), default log levels, report formats.

        targets/target_X.ini: Each file defines parameters for a specific hardware target or board variant.

            Trace32 connection details (IP address, port of the Trace32 instance controlling this target).

            Path to the ELF/AXF file to be loaded.

            CPU type for Trace32.

            Any specific CMM scripts for target setup.

            Memory regions of interest.

        test_suites/: (Optional) If some test suites require specific configurations not tied to a target.

    reports/: Generated by pytest (e.g., JUnit XML for CI, HTML reports for human review). This directory should be in .gitignore.

    logs/: Detailed execution logs from Python and potentially logs captured from Trace32. This directory should be in .gitignore.

    run_tests.py: The main command-line interface (CLI) for the framework.

        Uses argparse to parse command-line arguments (e.g., --target, --suite, --testcase, --report-format).

        Sets up logging.

        Loads the appropriate configurations.

        Invokes pytest programmatically or via subprocess with the selected tests and options.

    requirements.txt: Lists Python dependencies (e.g., pytest, pytest-html, configparser, any Trace32 Python API package if available, or ctypes which is built-in).

    pytest.ini: Configuration for pytest, e.g., default markers, paths, plugins.

    README.md: Instructions on setup, usage, contribution guidelines.

4. Where State Lives & How Services Connect

    Configuration State:

        Lives: In .ini (or .yaml) files within the config/ directory.

        Accessed: Loaded by config_loader.py at the start of a test run (triggered by run_tests.py or pytest fixtures). The loaded configuration is typically passed around or made available globally/contextually to test functions.

    Test Execution State (Runtime):

        Lives: Primarily in memory within the Python process running the tests.

            t32_connector.py object holds the current Trace32 connection status and API handles.

            pytest manages the state of test discovery, execution, and result collection.

            Variables within Python test functions hold temporary data for assertions.

        Trace32 Internal State: The Trace32 application itself maintains significant state about the target:

            Connection to the target.

            Loaded symbols and binaries.

            Breakpoint and watchpoint states.

            Current program counter, register values.

            This state is manipulated and queried by Python via the Remote API.

        File System State (Temporary):

            CMM scripts might create temporary files or logs if configured to do so.

            Test reports and logs are written to reports/ and logs/ directories towards the end of the test run.

    State Between Test Runs (Persistent):

        By default, this framework is largely stateless between independent runs. Each execution (e.g., a new pipeline job) starts fresh.

        Test Results: The primary "persistent" state artifacts are the generated reports (JUnit XML, HTML) and logs, which are stored on the file system and typically archived by the CI/CD system.

        Target Hardware State: The state of the embedded target itself can be persistent if not explicitly reset. Test cases should ensure the target is in a known state before execution, usually via reset commands sent through Trace32.

    How Services Connect:

        CI/CD Pipeline / User (CLI) -> Python Test Orchestrator (run_tests.py):

            Connection: The CI pipeline executes python run_tests.py [args] as a shell command. A user does the same from their terminal.

            Data: Arguments are passed via command-line flags. Environment variables can also be used. Results are read from files (reports/logs) generated by the orchestrator.

        Python Test Orchestrator (run_tests.py) -> Pytest Engine:

            Connection: run_tests.py typically invokes pytest either by importing and calling pytest.main() or by using subprocess.run(["pytest", ...]).

            Data: Test discovery paths, markers, and other pytest options are passed as arguments.

        Pytest Test Cases (tests/**/*.py) -> t32_connector.py:

            Connection: Python test functions import and instantiate (or receive via fixtures) the T32Connector class from t32_connector.py. They call its methods.

            Data: Method arguments (e.g., CMM script path, memory address, data to write) and return values (e.g., memory content, register value).

        t32_connector.py -> Trace32 Instance (Remote API):

            Connection: TCP/IP socket connection. The Python script acts as a client, and the Trace32 application (running with API <port> enabled) acts as the server. This connection traverses the VPN.

            Prerequisite: The VPN must be established before t32_connector.py attempts to connect to the Trace32 IP address. The framework usually assumes the VPN is externally managed.

            Data: Binary remote API commands are exchanged over the socket. Python sends commands like "execute CMM," "read memory," and Trace32 sends back responses/data.

        Python (t32_connector.py) -> .cmm Scripts:

            Connection (Indirect): Python instructs Trace32 (via API) to execute a specific .cmm script (e.g., using T32_ExecuteScript() or DO myscript.cmm via a generic command function).

            Data:

                Parameters can be passed to CMM scripts by setting Trace32 global variables (GLOBAL &varname) via API calls before executing the script.

                CMM scripts can write output to the Trace32 AREA window, which can then be read back by Python via API calls if needed, or write to files.

        Trace32 Instance -> Embedded Target Hardware:

            Connection: Physical debug interface (JTAG, SWD, BDM, etc.) connecting the Trace32 debugger probe (e.g., PowerTrace, CombiProbe) to the embedded target.

            Data: Low-level debug commands and data signals.

