"""
read music list


"""

import json

from objprint import op

import constants

ITEM_KEY = 'Tracks'
MUSIC_KEY = 'Apple Music'


def print_all_keys(filepath):
    with open(filepath, mode='rb') as fp:
        content = json.load(fp)

    key_list = []
    all_items = content['Tracks']

    for k, v in all_items.items():
        for kk, vv in v.items():
            if kk not in key_list:
                key_list.append(kk)
    op(key_list)


def load_apple_music_items(filepath):
    with open(filepath, mode='r', encoding='utf8') as fp:
        content = json.load(fp)

    music_items = content[ITEM_KEY]
    music_item_cnt = 0

    result_items = []
    schema_attrs = constants.get_schema_dict()

    for _, music_item_dict in music_items.items():
        if music_item_dict.get(MUSIC_KEY) is not True:
            continue
        music_item_cnt += 1
        result_dict = {}

        for attr_name, attr_value in schema_attrs.items():
            value = music_item_dict.get(attr_value)
            if value is None:
                continue
            result_dict[attr_name] = value

        op(result_dict)
        result_items.append(result_dict)

    return result_items


if __name__ == "__main__":
    # print_all_keys(r'C:\code\Py311\demos\202512\demo.json')
    load_apple_music_items(r'C:\code\Py311\demos\202512\demo.json')
