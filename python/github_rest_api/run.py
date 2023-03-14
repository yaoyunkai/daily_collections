"""


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
    "private",  # bool

    "owner_id",  # FK: owner.id
    "owner_login",
    "owner_html_url",

    "html_url",
    "description",
    "fork",  # bool
    "url",
    "languages_url",
    "created_at",  # datetime
    "updated_at",  # datetime
    "pushed_at",  # datetime
    "ssh_url",
    "clone_url",
    "homepage",
    "stargazers_count",  # int
    "watchers_count",  # int
    "forks_count",  # int
    "language",  # string or null
    "archived",  # bool
    "disabled",  # bool
    "visibility",
    # "topics"  # arrays / exclude
]

USER_HEADER = [
    "id",
    "login",
    "avatar_url",
    "url",
    "html_url",
    "repos_url",
    "type",
    "site_admin",  # bool
]

REPO_INSERT_SQL = """
insert into github_repo (id, `name`, full_name, private, owner_id, owner_login, owner_html_url, html_url, `description`,
                         fork, url, languages_url, created_at, updated_at, pushed_at, ssh_url, clone_url, homepage,
                         stargazers_count, watchers_count, forks_count, `language`, archived, disabled, visibility)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
REPO_UPDATE_SQL = """
update github_repo
set `name`           = %s,
    full_name        = %s,
    private          = %s,
    owner_id         = %s,
    owner_login      = %s,
    owner_html_url   = %s,
    html_url         = %s,
    `description`    = %s,
    fork             = %s,
    url              = %s,
    languages_url    = %s,
    created_at       = %s,
    updated_at       = %s,
    pushed_at        = %s,
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
where id = %s
"""


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
        url = 'https://api.github.com/user/starred?sort=created&per_page=50&page={}'.format(page)
        resp = requests.get(url, headers=headers)
        result = resp.json()
        if result:
            print('get page-{} repos'.format(page))
            for item in result:
                repo_data = []
                owner_data = item.get('owner', {})
                topics = item.get('topics', [])
                if topics:
                    topics = [i.lower() for i in topics]

                for repo_key in REPO_HEADER:

                    if repo_key in ['id', 'name']:
                        _value = item[repo_key]

                    elif repo_key in ['private', 'fork', 'archived', 'disabled']:
                        _value = item.get(repo_key, False)

                    elif repo_key in ['stargazers_count', 'watchers_count', 'forks_count']:
                        _value = item.get(repo_key, 0)

                    elif repo_key in ['created_at', 'updated_at', 'pushed_at']:
                        _value = item.get(repo_key, '2000-01-01 00:00:00')
                        _value = _value.replace('T', ' ').replace('Z', '')

                    elif repo_key in ['owner_id', 'owner_login', 'owner_html_url']:
                        _value = owner_data[repo_key.replace('owner_', '')]

                    else:
                        _value = item.get(repo_key)
                        _value = _value or ''

                    repo_data.append(_value)

                # print(repo_data)
                create_or_update_repo(mysql_conn, repo_data)
                create_or_update_user(mysql_conn, owner_data)
                update_repo_topics(mysql_conn, repo_data[0], topics)

            # marked
            # break
        else:
            print('saved all repos data')
            break


def create_or_update_repo(conn, info_list: list):
    cursor = conn.cursor()

    check_sql = """select id from github_repo where id = %s"""

    try:
        cursor.execute(check_sql, [info_list[0], ])
        exists = cursor.fetchone()
        if exists:
            cursor.execute(REPO_UPDATE_SQL, info_list[1:] + [info_list[0]])
        else:
            cursor.execute(REPO_INSERT_SQL, info_list)
        conn.commit()
    except Exception as e:
        print('db github_repo error: {}'.format(e))
        conn.rollback()


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
            # site_admin
            _value = info_dict.get(user_key, False)

        one_user_data.append(_value)

    cursor = conn.cursor()
    try:
        cursor.execute(check_sql, [one_user_data[0], ])
        result = cursor.fetchone()
        if result:
            cursor.execute(update_sql, one_user_data[1:] + [one_user_data[0]])
        else:
            cursor.execute(insert_sql, one_user_data)
        conn.commit()
    except Exception as e:
        print("db github_user error: {}".format(e))
        conn.rollback()


def update_repo_topics(conn, repo_id, topics: list):
    cursor = conn.cursor()

    delete_sql = """delete from github_repo_topic_rel where repo_id = %s"""
    insert_sql = """insert into github_repo_topic_rel (repo_id, topic_name) values (%s, %s)"""

    try:
        cursor.execute(delete_sql, [repo_id, ])
        for topic in topics:
            cursor.execute(insert_sql, [repo_id, topic])
        conn.commit()
    except Exception as e:
        print('db repo_topics error: {}'.format(e))
        conn.rollback()


if __name__ == '__main__':
    # get_mysql_conn()
    get_stars_api()
