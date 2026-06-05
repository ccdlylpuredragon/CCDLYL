"""Payment service module — refactored to use shared utilities."""

from utils.file_io import read_json, write_json
from utils.http import get, post
from utils.logging import get_logger
from utils.validation import FieldValidator

logger = get_logger("payment_service")

BASE_URL = "https://api.example.com/payments"


def process_payment(payment_data):
    """Process a payment via the API."""
    return post(BASE_URL, json=payment_data)


def fetch_payment(payment_id):
    """Fetch a payment from the API."""
    return get(f"{BASE_URL}/{payment_id}")


def refund_payment(payment_id):
    """Refund a payment via the API."""
    return post(f"{BASE_URL}/{payment_id}/refund")


def validate_payment_data(data):
    """Validate payment data before processing."""
    v = FieldValidator(data)
    v.require("amount", type_=(int, float), min_val=0, max_val=1000000)
    v.require("currency", type_=str, min_length=3, max_length=3)
    v.require("method", type_=str, choices=("credit_card", "debit_card", "bank_transfer"))
    return v.errors


def read_payment_config(filepath):
    """Read payment configuration from a JSON file."""
    return read_json(filepath)


def write_payment_config(filepath, data):
    """Write payment configuration to a JSON file."""
    return write_json(filepath, data)
