"""Integration tests verifying refactored services still work correctly."""

import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import validate_user_data, fetch_user
from services.order_service import validate_order_data, fetch_order
from services.payment_service import validate_payment_data
from services.notification_service import validate_email_data


def test_user_validation_valid():
    errors = validate_user_data({"name": "Alice", "email": "a@b.com"})
    assert errors == []


def test_user_validation_invalid():
    errors = validate_user_data({})
    assert "name is required" in errors
    assert "email is required" in errors


def test_order_validation_valid():
    errors = validate_order_data({"product_id": "SKU123", "quantity": 5})
    assert errors == []


def test_order_validation_invalid():
    errors = validate_order_data({"product_id": "", "quantity": 0})
    assert len(errors) > 0


def test_payment_validation_valid():
    errors = validate_payment_data({
        "amount": 99.99,
        "currency": "USD",
        "method": "credit_card",
    })
    assert errors == []


def test_payment_validation_invalid():
    errors = validate_payment_data({"amount": -1, "currency": "USDX", "method": "cash"})
    assert len(errors) > 0


def test_email_validation_valid():
    errors = validate_email_data({
        "recipient": "user@example.com",
        "subject": "Hello",
        "body": "World",
    })
    assert errors == []


def test_email_validation_invalid():
    errors = validate_email_data({})
    assert "recipient is required" in errors


def test_fetch_user_uses_shared_http():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "u1"}
    mock_response.raise_for_status = MagicMock()

    with patch("utils.http.requests.request", return_value=mock_response):
        result = fetch_user("u1")

    assert result == {"id": "u1"}


def test_fetch_order_uses_shared_http():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "o1"}
    mock_response.raise_for_status = MagicMock()

    with patch("utils.http.requests.request", return_value=mock_response):
        result = fetch_order("o1")

    assert result == {"id": "o1"}
