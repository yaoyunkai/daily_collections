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

import requests

with open('pass_keys.txt', mode='r') as __fp:
    passwd = __fp.read().strip()

REPO_HEADERS = [
    "id",
    "name",
    "full_name",
    "private",
    "owner_id",  # owner.id
    "html_url",
    "description",
    "fork",
    "url",
    "branches_url",
    "tags_url",
    "languages_url",
    "commits_url",
    "created_at",
    "updated_at",
    "pushed_at",
    "git_url",
    "ssh_url",
    "clone_url",
    "homepage",
    "stargazers_count",
    "watchers_count",
    "forks_count",
    "language",
    "archived",
    "disabled",
    "visibility",
    "topics"
]

USER_HEADER = [
    "id",
    "login",
    "avatar_url",
    "url",
    "html_url",
    "repos_url",
    "type",
    "site_admin",
]


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
            for item in result:
                one_data = []
                for repo_key in REPO_HEADERS:
                    # int key
                    if repo_key in ['private', 'fork', 'stargazers_count',
                                    'watchers_count', 'forks_count', 'archived', 'disabled']:
                        _value = item.get(repo_key, 0)
                        if type(_value) is bool:
                            _value = 1 if _value else 0

                    elif repo_key in ['created_at', 'updated_at', 'pushed_at']:
                        _value = item.get(repo_key, '2000-01-01 00:00:00')
                        _value = _value.replace('T', ' ').replace('Z', '')
                    elif repo_key == 'owner_id':
                        owner_data = item.get('owner', {})
                        _value = owner_data.get('id')
                    elif repo_key == 'topics':
                        pass
                    else:
                        _value = item.get(repo_key, '') or ''

                    if repo_key != 'topics':
                        one_data.append(_value)
            break
        else:
            print('saved all repos data')
            break


if __name__ == '__main__':
    get_stars_api()
    # pass
