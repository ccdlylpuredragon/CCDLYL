"""Shared HTTP request utilities with retry logic."""

import time

import requests

from utils.logging import get_logger

logger = get_logger(__name__)


def request_with_retry(method, url, max_retries=3, retry_delay=1, timeout=10, **kwargs):
    """Make an HTTP request with exponential backoff retry.

    Args:
        method: HTTP method ("get", "post", "put", "delete", etc.).
        url: The request URL.
        max_retries: Maximum number of attempts before raising.
        retry_delay: Base delay in seconds between retries (doubles each attempt).
        timeout: Request timeout in seconds.
        **kwargs: Additional arguments passed to requests.request().

    Returns:
        Parsed JSON response body.

    Raises:
        requests.exceptions.RequestException: If all retry attempts fail.
    """
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, timeout=timeout, **kwargs)
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


def get(url, **kwargs):
    """HTTP GET with retry."""
    return request_with_retry("get", url, **kwargs)


def post(url, **kwargs):
    """HTTP POST with retry."""
    return request_with_retry("post", url, **kwargs)
