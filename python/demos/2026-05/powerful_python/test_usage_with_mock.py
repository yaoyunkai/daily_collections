"""
test_usage_with_mock.py


created at 2026-05-20
"""

import unittest
from unittest.mock import Mock, patch

import requests


def get_user_info(user_id):
    """请求外部 API 获取用户信息"""
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


class TestUserService(unittest.TestCase):
    @patch("requests.get")
    def test_get_user_info_success(self, mock_get):
        """
        mock_get 假的方式来替换 requests.get

        """

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "Alice"}

        mock_get.return_value = mock_response

        result = get_user_info(1)

        self.assertEqual(result, {"id": 1, "name": "Alice"})
        mock_get.assert_called_once_with("https://api.example.com/users/1")


if __name__ == "__main__":
    unittest.main()
