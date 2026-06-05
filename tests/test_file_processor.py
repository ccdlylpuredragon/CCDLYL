"""Tests for app.file_processor — verifies errors propagate correctly."""

from pathlib import Path

import pytest

from app.file_processor import process_file


def test_process_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        process_file(tmp_path / "missing.txt")


def test_process_file_permission_denied(tmp_path: Path) -> None:
    restricted = tmp_path / "restricted.txt"
    restricted.write_text("hello", encoding="utf-8")
    restricted.chmod(0o000)
    try:
        with pytest.raises(PermissionError):
            process_file(restricted)
    finally:
        restricted.chmod(0o644)


def test_process_file_success(tmp_path: Path) -> None:
    f = tmp_path / "input.txt"
    f.write_text("  hello  \n  world  \n", encoding="utf-8")
    result = process_file(f)
    assert result == "hello\nworld"


def test_process_file_empty(tmp_path: Path) -> None:
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    result = process_file(f)
    assert result == ""
