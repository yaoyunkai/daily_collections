"""

Steam API


steamBD search
    根据类型区分
    是否在库中 ??? 不做强制要求
    是否有parent app id

"""
import configparser
import datetime
import json

import pandas
import requests

import save_license_to_excel

api_key = '---'
steam_id = '---'


def load_app_secure_key():
    global api_key, steam_id
    config = configparser.ConfigParser()
    config.read('personal.ini', encoding='utf8')

    if 'steam' not in config.sections():
        raise SystemExit('no such config')

    steam_item = config['steam']
    api_key = steam_item.get('api_key', '')
    steam_id = steam_item.get('steam_id', '')


load_app_secure_key()


def get_supported_apilist():
    base_url = 'https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/'
    params = {'key': api_key, }
    try:
        resp = requests.request('GET', base_url, params=params)
        if resp.status_code == 200:
            data = json.loads(resp.content)

        else:
            raise ValueError(f'API 返回的响应码不是 200')

    except Exception as e:
        print('Fatal Error')
        print(e)


def get_owned_games(include_appinfo=True, include_played_free_games=True):
    """
    params:
    include_appinfo
    include_played_free_games
    appids_filter                 似乎没用
    include_free_sub
    skip_unvetted_apps
    language
    include_extended_appinfo

    """

    base_url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
    method = 'GET'

    params = {'key': api_key,
              'steamid': steam_id}

    if include_appinfo:
        params['include_appinfo'] = True
    if include_played_free_games:
        params['include_played_free_games'] = True

    params['include_free_sub'] = True
    params['skip_unvetted_apps'] = False
    params['include_extended_appinfo'] = True

    results = []

    try:
        resp = requests.request(method, base_url, params=params)
        if resp.status_code == 200:
            data = json.loads(resp.content)
            data = data['response']
            game_count = data['game_count']
            game_items = data['games']  # list of dict
            print(f'一共获取了{game_count}条数据')
        else:
            raise ValueError(f'API 返回的响应码不是 200')

    except Exception as e:
        print('Fatal Error')
        print(e)
        return results

    # 时间单位是分钟
    for game_item in game_items:
        # pprint.pprint(game_item)
        _item = dict()
        _item['name'] = game_item['name']
        _item['appid'] = game_item['appid']
        _item['time_total'] = game_item.get('playtime_forever', 0)
        _item['time_2weeks'] = game_item.get('playtime_2weeks', 0)
        _item['time_total'] = round(_item['time_total'] / 60, 2)
        _item['time_2weeks'] = round(_item['time_2weeks'] / 60, 2)

        _item['last_played'] = game_item.get('rtime_last_played', None)
        if _item['last_played'] is not None:
            # local time
            _item['last_played'] = datetime.datetime.fromtimestamp(_item['last_played'])
            # _item['last_played'] = _item['last_played'].strftime("%Y-%m-%d %H:%M:%S")

        # pprint.pprint(_item)
        results.append(_item)

    return results


def save_owned_games(res_list: list):
    filename = 'steam_playtime_{}.xlsx'.format(save_license_to_excel.get_current_datetime())
    df = pandas.DataFrame(res_list, columns=['appid', 'name', 'time_total', 'time_2weeks', 'last_played'])
    df['appid'] = df['appid'].astype('int')
    df['time_total'] = df['time_total'].astype('float')
    df['time_2weeks'] = df['time_2weeks'].astype('float')
    df['last_played'] = pandas.to_datetime(df['last_played'])

    df.to_excel(filename, index=False)


if __name__ == '__main__':
    load_app_secure_key()
