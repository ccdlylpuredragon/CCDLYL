"""Order service module — refactored to use shared utilities."""

from utils.file_io import read_json, write_json
from utils.http import get, post
from utils.logging import get_logger
from utils.validation import FieldValidator

logger = get_logger("order_service")

BASE_URL = "https://api.example.com/orders"


def fetch_order(order_id):
    """Fetch an order from the API."""
    return get(f"{BASE_URL}/{order_id}")


def create_order(data):
    """Create an order via the API."""
    return post(BASE_URL, json=data)


def cancel_order(order_id):
    """Cancel an order via the API."""
    return post(f"{BASE_URL}/{order_id}/cancel")


def validate_order_data(data):
    """Validate order data before creating an order."""
    v = FieldValidator(data)
    v.require("product_id", type_=str, max_length=100)
    v.require("quantity", type_=int, min_val=1, max_val=1000)
    v.optional("notes", type_=str, max_length=500)
    return v.errors


def read_order_config(filepath):
    """Read order configuration from a JSON file."""
    return read_json(filepath)


def write_order_config(filepath, data):
    """Write order configuration to a JSON file."""
    return write_json(filepath, data)
