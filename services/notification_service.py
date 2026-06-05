"""Notification service module with duplicated patterns."""

import json
import logging
import time

import requests


def setup_logging():
    logger = logging.getLogger("notification_service")
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


def send_email(recipient, subject, body):
    """Send an email notification via the API with retry logic."""
    url = "https://api.example.com/notifications/email"
    data = {"recipient": recipient, "subject": subject, "body": body}
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


def send_sms(phone_number, message):
    """Send an SMS notification via the API with retry logic."""
    url = "https://api.example.com/notifications/sms"
    data = {"phone_number": phone_number, "message": message}
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


def fetch_notification_status(notification_id):
    """Fetch notification delivery status with retry logic."""
    url = f"https://api.example.com/notifications/{notification_id}/status"
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


def validate_email_data(data):
    """Validate email notification data."""
    errors = []

    if not data.get("recipient"):
        errors.append("recipient is required")
    elif not isinstance(data["recipient"], str):
        errors.append("recipient must be a string")
    elif "@" not in data["recipient"]:
        errors.append("recipient must be a valid email address")

    if not data.get("subject"):
        errors.append("subject is required")
    elif not isinstance(data["subject"], str):
        errors.append("subject must be a string")
    elif len(data["subject"]) > 200:
        errors.append("subject must be at most 200 characters")

    if not data.get("body"):
        errors.append("body is required")
    elif not isinstance(data["body"], str):
        errors.append("body must be a string")
    elif len(data["body"]) > 10000:
        errors.append("body must be at most 10000 characters")

    return errors


def read_notification_config(filepath):
    """Read notification configuration from a JSON file."""
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


def write_notification_config(filepath, data):
    """Write notification configuration to a JSON file."""
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
