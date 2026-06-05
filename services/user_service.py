"""User service module — refactored to use shared utilities."""

from utils.file_io import read_json, write_json
from utils.http import get, post
from utils.logging import get_logger
from utils.validation import FieldValidator

logger = get_logger("user_service")

BASE_URL = "https://api.example.com/users"


def fetch_user(user_id):
    """Fetch a user from the API."""
    return get(f"{BASE_URL}/{user_id}")


def create_user(data):
    """Create a user via the API."""
    return post(BASE_URL, json=data)


def validate_user_data(data):
    """Validate user data before creating a user."""
    v = FieldValidator(data)
    v.require("name", type_=str, max_length=100)
    v.require("email", type_=str, pattern="@")
    v.optional("age", type_=int, min_val=0, max_val=150)
    return v.errors


def read_user_config(filepath):
    """Read user configuration from a JSON file."""
    return read_json(filepath)


def write_user_config(filepath, data):
    """Write user configuration to a JSON file."""
    return write_json(filepath, data)
