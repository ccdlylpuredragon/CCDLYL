"""User service module with duplicated patterns."""

import json
import logging
import time

import requests


def setup_logging():
    logger = logging.getLogger("user_service")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = setup_logging()


def fetch_user(user_id):
    """Fetch a user from the API with retry logic."""
    url = f"https://api.example.com/users/{user_id}"
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}"
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                logger.error(f"All {max_retries} attempts failed for {url}")
                raise


def create_user(data):
    """Create a user via the API with retry logic."""
    url = "https://api.example.com/users"
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}"
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                logger.error(f"All {max_retries} attempts failed for {url}")
                raise


def validate_user_data(data):
    """Validate user data before creating a user."""
    errors = []

    if not data.get("name"):
        errors.append("name is required")
    elif not isinstance(data["name"], str):
        errors.append("name must be a string")
    elif len(data["name"]) > 100:
        errors.append("name must be at most 100 characters")

    if not data.get("email"):
        errors.append("email is required")
    elif not isinstance(data["email"], str):
        errors.append("email must be a string")
    elif "@" not in data["email"]:
        errors.append("email must be a valid email address")

    if data.get("age") is not None:
        if not isinstance(data["age"], int):
            errors.append("age must be an integer")
        elif data["age"] < 0 or data["age"] > 150:
            errors.append("age must be between 0 and 150")

    return errors


def read_user_config(filepath):
    """Read user configuration from a JSON file."""
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


def write_user_config(filepath, data):
    """Write user configuration to a JSON file."""
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
