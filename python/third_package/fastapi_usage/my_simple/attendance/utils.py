"""


Created at 2023/7/14
"""

import re


def is_valid_english_name(person_name: str) -> bool:
    return re.match(r"^[A-Za-z\s'-]+$", person_name) is not None


def is_valid_chinese_name(person_name: str) -> bool:
    return re.match(r"^[\u4e00-\u9fa5]{2,4}$", person_name) is not None
