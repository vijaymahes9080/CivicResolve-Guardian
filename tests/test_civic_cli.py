import subprocess
import sys
import pytest

def test_civic_cli_help():
    res = subprocess.run(
        [sys.executable, "backend/civic_cli.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "CivicResolve Guardian Municipal Administrative CLI" in res.stdout

def test_civic_cli_list_tenants():
    res = subprocess.run(
        [sys.executable, "backend/civic_cli.py", "list-tenants"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "[GCC]" in res.stdout
    assert "Greater Chennai Corporation" in res.stdout

def test_civic_cli_fuzzer_audit():
    res = subprocess.run(
        [sys.executable, "backend/civic_cli.py", "fuzzer-audit"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "Defense Success Rate: 100.0%" in res.stdout
