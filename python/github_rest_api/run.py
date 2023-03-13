"""

id
node_id
name
fullname
private

onwer.login
onwer.id
onwer.html_url
onwer.type

html_url
description
fork
url
languages_url
commits_url
git_commits_url
ssh_url
clone_url
homepage
stargazers_count
watchers_count
language
forks_count
archived
disabled

topics : array

updated_at
created_at

Created at 2023/3/11
"""
import json

import requests

with open('pass_keys.txt', mode='r') as __fp:
    passwd = __fp.read().strip()


def get_stars_api():
    """
    curl -L \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer <YOUR-TOKEN>"\
      -H "X-GitHub-Api-Version: 2022-11-28" \
      https://api.github.com/user/starred

    """
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer {}'.format(passwd),
        'X-GitHub-Api-Version': '2022-11-28'
    }

    page = 0
    while True:
        page += 1
        url = 'https://api.github.com/user/starred?per_page=50&page={}'.format(page)
        resp = requests.get(url, headers=headers)
        result = resp.json()
        if result:
            print('get page:{} repos'.format(page))
            with open('data/repos-{}.json'.format(page), mode='a') as fp:
                json.dump(result, fp)
        else:
            print('saved all repos data')
            break


if __name__ == '__main__':
    get_stars_api()
    # pass
