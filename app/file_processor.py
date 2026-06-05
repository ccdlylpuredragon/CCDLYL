"""File processing with proper error handling.

Demonstrates:
- Context managers for reliable resource cleanup
- Specific exception types instead of bare ``except``
- Exception chaining (``raise ... from ...``)
- Never silently swallowing errors
- Logging before propagating
"""

import logging
from pathlib import Path

from app.exceptions import ParseError, ProcessingError

logger = logging.getLogger(__name__)


def process_file(path: str | Path) -> str:
    """Read a text file, process its content, and return the result.

    Parameters
    ----------
    path:
        Path to the input file.

    Returns
    -------
    str
        The processed content.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    PermissionError
        If the current user cannot read *path*.
    ParseError
        If the file content cannot be parsed.
    ProcessingError
        If processing fails for any other reason.
    """
    file_path = Path(path)
    logger.info("Processing file: %s", file_path)

    lines = _read_lines(file_path)
    processed = _transform_lines(lines)
    return "\n".join(processed)


def _read_lines(path: Path) -> list[str]:
    """Read all lines from *path*.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    PermissionError
        If the file is not readable.
    ParseError
        If the file cannot be decoded as UTF-8.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error("File not found: %s", path)
        raise
    except PermissionError:
        logger.error("Permission denied: %s", path)
        raise
    except UnicodeDecodeError as exc:
        raise ParseError(
            f"Cannot decode {path} as UTF-8: {exc}"
        ) from exc

    return text.splitlines()


def _transform_lines(lines: list[str]) -> list[str]:
    """Apply transformations to each line.

    Raises
    ------
    ProcessingError
        If a line cannot be processed.
    """
    results: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        try:
            results.append(_process_line(line))
        except ValueError as exc:
            raise ProcessingError(
                f"Error processing line {lineno}: {exc}"
            ) from exc
    return results


def _process_line(line: str) -> str:
    """Process a single line — strip whitespace and normalize."""
    return line.strip()
