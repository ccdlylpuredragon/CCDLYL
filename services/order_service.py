"""Order service module with duplicated patterns."""

import json
import logging
import time

import requests


def setup_logging():
    logger = logging.getLogger("order_service")
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


def fetch_order(order_id):
    """Fetch an order from the API with retry logic."""
    url = f"https://api.example.com/orders/{order_id}"
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


def create_order(data):
    """Create an order via the API with retry logic."""
    url = "https://api.example.com/orders"
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


def cancel_order(order_id):
    """Cancel an order via the API with retry logic."""
    url = f"https://api.example.com/orders/{order_id}/cancel"
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.post(url, timeout=10)
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


def validate_order_data(data):
    """Validate order data before creating an order."""
    errors = []

    if not data.get("product_id"):
        errors.append("product_id is required")
    elif not isinstance(data["product_id"], str):
        errors.append("product_id must be a string")
    elif len(data["product_id"]) > 100:
        errors.append("product_id must be at most 100 characters")

    if not data.get("quantity"):
        errors.append("quantity is required")
    elif not isinstance(data["quantity"], int):
        errors.append("quantity must be an integer")
    elif data["quantity"] < 1 or data["quantity"] > 1000:
        errors.append("quantity must be between 1 and 1000")

    if data.get("notes") is not None:
        if not isinstance(data["notes"], str):
            errors.append("notes must be a string")
        elif len(data["notes"]) > 500:
            errors.append("notes must be at most 500 characters")

    return errors


def read_order_config(filepath):
    """Read order configuration from a JSON file."""
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


def write_order_config(filepath, data):
    """Write order configuration to a JSON file."""
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
