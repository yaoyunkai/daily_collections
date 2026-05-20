"""
test_angle.py

python -m unittest test_angle.py


python.demos.2026-05.powerful_python.test_angle
test_angle


created at 2026-05-19
"""

import unittest

from angles import Angle


class TestAngle(unittest.TestCase):
    def test_degrees(self):
        small_angle = Angle(60)
        self.assertEqual(60, small_angle.degrees)
        self.assertTrue(small_angle.is_acute())

        big_angle = Angle(320)
        self.assertFalse(big_angle.is_acute())

        f_angle = Angle(1081)
        self.assertEqual(1, f_angle.degrees)

    def test_arithmetic(self):
        small_angle = Angle(60)
        big_angle = Angle(320)
        total_angle = small_angle + big_angle

        self.assertEqual(20, total_angle.degrees, "adding angles with wrap-around")


if __name__ == "__main__":
    unittest.main()
