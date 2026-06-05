import subprocess
import sys


def test_hello_output():
    result = subprocess.run(
        [sys.executable, "hello.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Hello World!" in result.stdout
