"""Tests for the shared HTTP utility."""

import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from utils.http import request_with_retry, get, post


def test_get_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "Test"}
    mock_response.raise_for_status = MagicMock()

    with patch("utils.http.requests.request", return_value=mock_response) as mock_req:
        result = get("https://api.example.com/test")

    assert result == {"id": 1, "name": "Test"}
    mock_req.assert_called_once_with("get", "https://api.example.com/test", timeout=10)


def test_post_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 2, "created": True}
    mock_response.raise_for_status = MagicMock()

    with patch("utils.http.requests.request", return_value=mock_response) as mock_req:
        result = post("https://api.example.com/test", json={"name": "New"})

    assert result == {"id": 2, "created": True}
    mock_req.assert_called_once_with(
        "post", "https://api.example.com/test", timeout=10, json={"name": "New"}
    )


@patch("utils.http.time.sleep")
def test_retry_on_failure(mock_sleep):
    mock_response = MagicMock()
    mock_response.json.return_value = {"ok": True}
    mock_response.raise_for_status = MagicMock()

    with patch("utils.http.requests.request") as mock_req:
        mock_req.side_effect = [
            requests.exceptions.ConnectionError("fail"),
            mock_response,
        ]
        result = request_with_retry("get", "https://api.example.com/test")

    assert result == {"ok": True}
    assert mock_req.call_count == 2
    mock_sleep.assert_called_once_with(1)


@patch("utils.http.time.sleep")
def test_all_retries_exhausted(mock_sleep):
    with patch("utils.http.requests.request") as mock_req:
        mock_req.side_effect = requests.exceptions.ConnectionError("fail")
        try:
            request_with_retry("get", "https://api.example.com/test", max_retries=3)
            assert False, "Should have raised"
        except requests.exceptions.ConnectionError:
            pass

    assert mock_req.call_count == 3
