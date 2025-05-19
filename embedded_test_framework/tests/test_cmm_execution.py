import pytest
import os

def test_run_hello_cmm(t32_session):
    """Tests executing a simple CMM script."""
    assert t32_session.is_connected, "T32 session not connected at start of CMM test"

    # Construct an absolute path to the CMM script
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    script_path = os.path.join(project_root, "cmm_scripts", "common", "hello.cmm")
    
    assert os.path.exists(script_path), f"CMM script not found at: {script_path}"

    status = t32_session.run_cmm_script(script_path)
    assert status == 0, f"run_cmm_script returned non-zero status: {status}" 