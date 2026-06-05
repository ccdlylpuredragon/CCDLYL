"""Shared file I/O utilities with error handling."""

import json

from utils.logging import get_logger

logger = get_logger(__name__)


def read_json(filepath):
    """Read and parse a JSON file with comprehensive error handling.

    Args:
        filepath: Path to the JSON file.

    Returns:
        Parsed JSON content as a dict, or empty dict on failure.
    """
    try:
        with open(filepath, "r") as f:
            config = json.load(f)
        logger.info(f"Successfully loaded config from {filepath}")
        return config
    except FileNotFoundError:
        logger.error(f"Config file not found: {filepath}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file {filepath}: {e}")
        return {}
    except PermissionError:
        logger.error(f"Permission denied reading config file: {filepath}")
        return {}


def write_json(filepath, data):
    """Write data to a JSON file with error handling.

    Args:
        filepath: Path to the JSON file.
        data: Data to serialize as JSON.

    Returns:
        True on success, False on failure.
    """
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Successfully wrote config to {filepath}")
        return True
    except PermissionError:
        logger.error(f"Permission denied writing config file: {filepath}")
        return False
    except OSError as e:
        logger.error(f"OS error writing config file {filepath}: {e}")
        return False
