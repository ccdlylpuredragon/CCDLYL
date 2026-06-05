"""Custom exception hierarchy for the CCDLYL application.

Provides specific exception types so callers can handle errors granularly
instead of catching broad ``Exception`` or silently swallowing failures.
"""


class AppError(Exception):
    """Base exception for all application errors."""


class ConfigError(AppError):
    """Raised when configuration is missing or invalid."""


class ParseError(AppError):
    """Raised when file content cannot be parsed."""


class ProcessingError(AppError):
    """Raised when a processing step fails."""


class ValidationError(AppError):
    """Raised when data fails validation."""
