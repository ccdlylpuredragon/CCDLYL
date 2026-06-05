"""Tests for the shared file I/O utility."""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_io import read_json, write_json


def test_read_json_success():
    data = {"key": "value", "number": 42}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        filepath = f.name

    try:
        result = read_json(filepath)
        assert result == data
    finally:
        os.unlink(filepath)


def test_read_json_file_not_found():
    result = read_json("/nonexistent/path.json")
    assert result == {}


def test_read_json_invalid_json():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("not valid json{{{")
        filepath = f.name

    try:
        result = read_json(filepath)
        assert result == {}
    finally:
        os.unlink(filepath)


def test_write_json_success():
    data = {"hello": "world"}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        filepath = f.name

    try:
        result = write_json(filepath, data)
        assert result is True

        with open(filepath) as f:
            written = json.load(f)
        assert written == data
    finally:
        os.unlink(filepath)


def test_write_json_permission_error(tmp_path):
    filepath = str(tmp_path / "readonly.json")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("{}")
    os.chmod(filepath, 0o444)

    try:
        result = write_json(filepath, {"new": "data"})
        assert result is False
    finally:
        os.chmod(filepath, 0o644)
        os.unlink(filepath)
