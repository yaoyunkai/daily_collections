"""


Created at 2023/8/15
"""
import json

import requests

if __name__ == '__main__':
    r = requests.get("http://localhost:8000/items/?cc=1234&dd=23", headers={'dd': '213'})

    print(json.loads(r.content))
