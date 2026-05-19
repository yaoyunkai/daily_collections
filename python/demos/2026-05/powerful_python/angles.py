"""
angles.py


created at 2026-05-19
"""

from typing import Self


class Angle(object):
    def __init__(self, val):
        self.degrees = val % 360

    def is_acute(self):
        """
        是否是锐角
        """
        return self.degrees < 90

    def __add__(self, other: "Self"):
        return Angle(self.degrees + other.degrees)
