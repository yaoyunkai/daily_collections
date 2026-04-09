"""
new_utils.py


created at 2026-04-09
"""

import pendulum


def get_current_time():
    return pendulum.now()


def get_local_tz():
    return pendulum.local_timezone()


if __name__ == "__main__":
    print(get_current_time())
