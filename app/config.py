"""Configuration loading with proper error handling.

Demonstrates:
- Exception chaining (``raise ... from ...``)
- Specific exception types instead of broad catches
- Logging errors before propagating
"""

import json
import logging
from pathlib import Path
from typing import Any

from app.exceptions import ConfigError

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("config.json")


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load JSON configuration from *path*.

    Parameters
    ----------
    path:
        Path to the config file.  Falls back to ``config.json`` in the
        current directory when *None*.

    Returns
    -------
    dict[str, Any]
        Parsed configuration dictionary.

    Raises
    ------
    FileNotFoundError
        If the config file does not exist.
    ConfigError
        If the file exists but cannot be parsed or validated.
    """
    config_path = path or DEFAULT_CONFIG_PATH

    try:
        raw = config_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.debug("Config file not found at %s", config_path)
        raise
    except OSError as exc:
        raise ConfigError(
            f"Unable to read config file {config_path}"
        ) from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"Invalid JSON in {config_path}: {exc.msg} "
            f"(line {exc.lineno}, col {exc.colno})"
        ) from exc

    if not isinstance(data, dict):
        raise ConfigError(
            f"Expected a JSON object in {config_path}, "
            f"got {type(data).__name__}"
        )

    _validate_config(data)
    return data


def _validate_config(data: dict[str, Any]) -> None:
    """Run basic validation on the parsed config dictionary.

    Raises
    ------
    ConfigError
        If required keys are missing or values have wrong types.
    """
    for key in ("input_path",):
        if key in data and not isinstance(data[key], str):
            raise ConfigError(
                f"Config key {key!r} must be a string, "
                f"got {type(data[key]).__name__}"
            )
