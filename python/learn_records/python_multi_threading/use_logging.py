"""
use_logging.py


created at 2026-04-07
"""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(threadName)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",  # 使用 T 分隔日期和时间
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("a")
    logger.info("b")
    logger.info("c")
