"""


Created at 2023/3/11
"""
import json
import pprint

import requests

passwd = 'xxx'


def test_connection():
    _header = {
        # 'Accept: application/vnd.github+json',
        # 'Authorization: Bearer YOUR-TOKEN',
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer {}'.format(passwd),
    }

    url = 'https://api.github.com/repos/octocat/Spoon-Knife/issues'
    resp = requests.get(url, headers=_header)
    pprint.pprint(
        json.loads(resp.content)
    )


def get_stars():
    """
    curl -L \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer <YOUR-TOKEN>"\
      -H "X-GitHub-Api-Version: 2022-11-28" \
      https://api.github.com/user/starred
    """
    for i in range(1, 7):
        url = 'https://api.github.com/user/starred?per_page=100&page={}'.format(i)
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer {}'.format(passwd),
            'X-GitHub-Api-Version': '2022-11-28'
        }
        resp = requests.get(url, headers=headers)
        fp = open('stars{}.json'.format(i), mode='ab')
        fp.write(resp.content)
        fp.close()


if __name__ == '__main__':
    get_stars()
