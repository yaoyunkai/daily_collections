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

import MySQLdb
import requests

with open('pass_keys.txt', mode='r') as __fp:
    passwd = __fp.read().strip()

REPO_HEADER = [
    "id",
    "name",
    "full_name",
    "private",  # ture or false 0-1
    "owner_id",  # FK: owner.id
    "html_url",
    "description",
    "fork",  # ture or false 0-1
    "url",
    "branches_url",
    "tags_url",
    "languages_url",
    "commits_url",
    "created_at",  # datetime
    "updated_at",  # datetime
    "pushed_at",  # datetime
    "git_url",
    "ssh_url",
    "clone_url",
    "homepage",
    "stargazers_count",  # int
    "watchers_count",  # int
    "forks_count",  # int
    "language",  # string or null
    "archived",  # ture or false 0-1
    "disabled",  # ture or false 0-1
    "visibility",
    "topics"  # arrays / exclude
]

USER_HEADER = [
    "id",
    "login",
    "avatar_url",
    "url",
    "html_url",
    "repos_url",
    "type",
    "site_admin",  # ture or false 0-1
]


def get_mysql_conn(db_name='demo3'):
    return MySQLdb.connect(host='localhost', port=3306, user='root', password='password', database=db_name)


def get_stars_api():
    """
    curl -L \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer <YOUR-TOKEN>"\
      -H "X-GitHub-Api-Version: 2022-11-28" \
      https://api.github.com/user/starred

    """
    mysql_conn = get_mysql_conn()

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
                one_repo_data = []

                for repo_key in REPO_HEADER:
                    _value = None  # just for Pycharm hint

                    if repo_key == 'id':
                        _value = item['id']
                    elif repo_key in ['private', 'fork', 'archived', 'disabled']:
                        _value = item.get(repo_key, False)
                    elif repo_key in ['stargazers_count', 'watchers_count', 'forks_count']:
                        _value = item.get(repo_key, 0)
                    elif repo_key in ['created_at', 'updated_at', 'pushed_at']:
                        _value = item.get(repo_key, '2000-01-01 00:00:00')
                        _value = _value.replace('T', ' ').replace('Z', '')
                    elif repo_key == 'owner_id':
                        _owner_data = item.get('owner', {})
                        _value = _owner_data['id']
                        # update or create User
                        create_or_update_user(mysql_conn, _owner_data)

                    elif repo_key == 'topics':
                        topics = item.get(repo_key, [])
                        update_repo_topics(mysql_conn, item['id'], topics)

                    else:
                        _value = item.get(repo_key)
                        _value = _value or ''

                    if repo_key != 'topics':
                        one_repo_data.append(_value)

                # update or create Repo
                # print(one_repo_data)
                create_or_update_repo(mysql_conn, one_repo_data)
        else:
            print('saved all repos data')
            break


def create_or_update_user(conn, info_dict: dict):
    """
    github_user

    """
    insert_sql = """insert into github_user (id, login, avatar_url, url, html_url, repos_url, type, site_admin)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)"""

    update_sql = """update github_user
                    set login      = %s,
                        avatar_url = %s,
                        url= %s,
                        html_url   = %s,
                        repos_url  = %s,
                        type= %s,
                        site_admin = %s
                    where id = %s"""

    check_sql = """select id from github_user where id = %s"""

    one_user_data = []

    for user_key in USER_HEADER:
        if user_key == 'id':
            _value = info_dict['id']

        elif user_key in ['login', 'avatar_url', 'url', 'html_url', 'repos_url', 'type']:
            _value = info_dict.get(user_key) or ''
        else:
            _value = info_dict.get(user_key, False)

        one_user_data.append(_value)

    user_id = one_user_data[0]
    cursor = conn.cursor()
    try:
        cursor.execute(check_sql, [user_id, ])
        result = cursor.fetchone()
        if result:
            cursor.execute(update_sql, one_user_data[1:] + [user_id])
        else:
            cursor.execute(insert_sql, one_user_data)
        conn.commit()
    except Exception as e:
        print("github_user error: {}".format(e))
        conn.rollback()


def create_or_update_repo(conn, info_list: list):
    # repo_id = info_list[0]

    insert_sql = """
    insert into github_repo
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s)
    """

    update_sql = """
    update github_repo
    set `name`           = %s,
        full_name        = %s,
        private          = %s,
        owner_id         = %s,
        html_url         = %s,
        `description`    = %s,
        fork             = %s,
        url              = %s,
        branches_url     = %s,
        tags_url         = %s,
        languages_url    = %s,
        commits_url      = %s,
        created_at       = %s,
        updated_at       = %s,
        pushed_at        = %s,
        git_url          = %s,
        ssh_url          = %s,
        clone_url        = %s,
        homepage         = %s,
        stargazers_count = %s,
        watchers_count   = %s,
        forks_count      = %s,
        `language`       = %s,
        archived         = %s,
        disabled         = %s,
        visibility       = %s
    where id = %s"""

    check_sql = """select id from github_repo where id = %s"""

    repo_id = info_list[0]
    cursor = conn.cursor()
    try:
        cursor.execute(check_sql, [repo_id, ])
        result = cursor.fetchone()
        if result:
            cursor.execute(update_sql, info_list[1:] + [repo_id])
        else:
            cursor.execute(insert_sql, info_list)
        conn.commit()
    except Exception as e:
        print("github_repo error: {}".format(e))
        conn.rollback()


def update_repo_topics(conn, repo_id, topics: list):
    # save topic to github_topic if not exists
    # update or Create Repo topics
    insert_sql = """insert into github_topic (topic) values (%s)"""
    check_sql = """select id, topic from github_topic where topic = %s"""
    delete_sql = """delete from guthub_repo_topic_rel where repo_id = %s"""

    insert_topic_rel = """insert into guthub_repo_topic_rel (repo_id, topic_id, topic_name)
                          values (%s, %s, %s) """

    cursor = conn.cursor()
    try:
        cursor.execute(delete_sql, [repo_id, ])

        for topic in topics:
            cursor.execute(check_sql, [topic, ])
            result = cursor.fetchone()  # (id, topic)
            if not result:
                cursor.execute(insert_sql, [topic, ])
                result = [repo_id, cursor.lastrowid, topic]
            else:
                result = [repo_id, result[0], result[1]]
            cursor.execute(insert_topic_rel, result)
        conn.commit()
    except Exception as e:
        print("error: {}".format(e))
        conn.rollback()


if __name__ == '__main__':
    # get_mysql_conn()
    get_stars_api()
