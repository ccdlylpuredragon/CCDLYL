import subprocess
import sys

from hello import hello, main


def test_hello_returns_greeting():
    """Test that hello() returns the expected greeting string."""
    assert hello() == "Hello World!"


def test_hello_return_type():
    """Test that hello() returns a string."""
    assert isinstance(hello(), str)


def test_main_prints_greeting(capsys):
    """Test that main() prints 'Hello World!' to stdout."""
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World!"


def test_main_no_stderr(capsys):
    """Test that main() produces no output on stderr."""
    main()
    captured = capsys.readouterr()
    assert captured.err == ""


def test_script_execution():
    """Test that hello.py runs correctly as a script."""
    result = subprocess.run(
        [sys.executable, "hello.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello World!"


def test_script_no_errors():
    """Test that hello.py produces no errors when run as a script."""
    result = subprocess.run(
        [sys.executable, "hello.py"],
        capture_output=True,
        text=True,
    )
    assert result.stderr == ""


def test_syntax_valid():
    """Test that hello.py has valid Python syntax."""
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", "hello.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
