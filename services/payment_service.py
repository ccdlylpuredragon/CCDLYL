"""Payment service module with duplicated patterns."""

import json
import logging
import time

import requests


def setup_logging():
    logger = logging.getLogger("payment_service")
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


def process_payment(payment_data):
    """Process a payment via the API with retry logic."""
    url = "https://api.example.com/payments"
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payment_data, timeout=10)
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


def fetch_payment(payment_id):
    """Fetch a payment from the API with retry logic."""
    url = f"https://api.example.com/payments/{payment_id}"
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


def refund_payment(payment_id):
    """Refund a payment via the API with retry logic."""
    url = f"https://api.example.com/payments/{payment_id}/refund"
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


def validate_payment_data(data):
    """Validate payment data before processing."""
    errors = []

    if not data.get("amount"):
        errors.append("amount is required")
    elif not isinstance(data["amount"], (int, float)):
        errors.append("amount must be a number")
    elif data["amount"] <= 0:
        errors.append("amount must be positive")
    elif data["amount"] > 1000000:
        errors.append("amount must be at most 1000000")

    if not data.get("currency"):
        errors.append("currency is required")
    elif not isinstance(data["currency"], str):
        errors.append("currency must be a string")
    elif len(data["currency"]) != 3:
        errors.append("currency must be a 3-letter code")

    if not data.get("method"):
        errors.append("method is required")
    elif data["method"] not in ("credit_card", "debit_card", "bank_transfer"):
        errors.append("method must be credit_card, debit_card, or bank_transfer")

    return errors


def read_payment_config(filepath):
    """Read payment configuration from a JSON file."""
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


def write_payment_config(filepath, data):
    """Write payment configuration to a JSON file."""
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
