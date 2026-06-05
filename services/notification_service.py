"""Notification service module — refactored to use shared utilities."""

from utils.file_io import read_json, write_json
from utils.http import get, post
from utils.logging import get_logger
from utils.validation import FieldValidator

logger = get_logger("notification_service")

BASE_URL = "https://api.example.com/notifications"


def send_email(recipient, subject, body):
    """Send an email notification via the API."""
    data = {"recipient": recipient, "subject": subject, "body": body}
    return post(f"{BASE_URL}/email", json=data)


def send_sms(phone_number, message):
    """Send an SMS notification via the API."""
    data = {"phone_number": phone_number, "message": message}
    return post(f"{BASE_URL}/sms", json=data)


def fetch_notification_status(notification_id):
    """Fetch notification delivery status."""
    return get(f"{BASE_URL}/{notification_id}/status")


def validate_email_data(data):
    """Validate email notification data."""
    v = FieldValidator(data)
    v.require("recipient", type_=str, pattern="@")
    v.require("subject", type_=str, max_length=200)
    v.require("body", type_=str, max_length=10000)
    return v.errors


def read_notification_config(filepath):
    """Read notification configuration from a JSON file."""
    return read_json(filepath)


def write_notification_config(filepath, data):
    """Write notification configuration to a JSON file."""
    return write_json(filepath, data)
