"""Tests for app.config — verifies errors are properly raised, not swallowed."""

import json
from pathlib import Path

import pytest

from app.config import load_config
from app.exceptions import ConfigError


def test_load_config_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nonexistent.json")


def test_load_config_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{invalid", encoding="utf-8")
    with pytest.raises(ConfigError, match="Invalid JSON"):
        load_config(bad)


def test_load_config_non_object(tmp_path: Path) -> None:
    arr = tmp_path / "array.json"
    arr.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(ConfigError, match="Expected a JSON object"):
        load_config(arr)


def test_load_config_bad_value_type(tmp_path: Path) -> None:
    bad_type = tmp_path / "bad_type.json"
    bad_type.write_text(json.dumps({"input_path": 123}), encoding="utf-8")
    with pytest.raises(ConfigError, match="must be a string"):
        load_config(bad_type)


def test_load_config_success(tmp_path: Path) -> None:
    good = tmp_path / "config.json"
    good.write_text(json.dumps({"input_path": "data/input.txt"}), encoding="utf-8")
    result = load_config(good)
    assert result == {"input_path": "data/input.txt"}
