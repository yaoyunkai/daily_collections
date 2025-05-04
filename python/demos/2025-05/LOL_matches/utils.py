"""


created at 2025/5/4
"""
import json

SPELL_MAP = {
    '21': '屏障'
}

PERK_MAP = {
    8100: '主宰',
    8300: '启迪',
    8000: '精密',
    8400: '坚决',
    8200: '巫术',
    0: '未知'
}

ITEM_MAP = {
    # '1001': '鞋子'
}


def get_item_name(item_id: int):
    """
    match record key is int
    local data is str

    :param item_id:
    :return:
    """
    item_id = str(item_id)

    if item_id == '0':
        return ''

    if item_id not in ITEM_MAP:
        with open('item_15.9.1_data.json', encoding='utf8') as f:
            row_data = json.load(f)
            row_data = row_data['data']

            for inner_id, item_item in row_data.items():
                if item_id == inner_id:
                    item_name = item_item['name']
                    ITEM_MAP[item_id] = item_name
                    return item_name
            else:
                print(f'item id: {item_id} not found')
                item_name = '未知装备'
                ITEM_MAP[item_id] = item_name
                return item_name

    else:
        return ITEM_MAP[item_id]


def get_spell_name(spell):
    """
    key is str

    :param spell:
    :return:
    """

    spell = str(spell)
    if spell not in SPELL_MAP:
        with open('spell_data.json', encoding='utf8') as f:
            row_data = json.load(f)
            row_data = row_data['data']

            for _, item in row_data.items():
                if item['key'] == spell:
                    name = item['name']

                    SPELL_MAP[spell] = name
                    return name
    else:
        return SPELL_MAP[spell]
