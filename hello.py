"""Entry point for the CCDLYL application."""

import logging
import sys

from app.config import load_config
from app.file_processor import process_file

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main() -> int:
    setup_logging()
    logger.info("Starting CCDLYL application")

    try:
        config = load_config()
    except FileNotFoundError:
        logger.warning("No config file found, using defaults")
        config = {}
    except ValueError as exc:
        logger.error("Invalid configuration: %s", exc)
        return 1

    input_path = config.get("input_path", "data/input.txt")
    try:
        result = process_file(input_path)
    except FileNotFoundError:
        logger.error("Input file not found: %s", input_path)
        return 1
    except PermissionError:
        logger.error("Permission denied reading: %s", input_path)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
