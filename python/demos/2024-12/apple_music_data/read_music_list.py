"""
read music list

Track ID           : personal track id
Name               : 歌曲名称
Artist             : 艺人
Album Artist       : 专辑艺人
Composer           : 作曲者      &  ,
Explicit           : E标
Compilation        : 专辑是多个艺人的歌曲合辑

Album              : 专辑
Genre              : 类型
Kind               : 文件类型
Size               : 文件大小
Total Time         : 文件时长
Disc Number        : 光盘编号
Disc Count

Track Number / Track Count  : 音轨
Year                   : 发行年份
BPM                    : ????  每分钟节拍数

Date Modified          : 修改日期   UTC 时间
Date Added             : 添加日期

Bit Rate
Sample Rate

Play Count             : 播放次数
Play Date UTC          : 上次播放时间   2024-01-07T15:15:59Z
Skip Count
Skip Date
Release Date            : 1986-02-12T12:00:00Z
Rating                   : 评分
Album Rating              : 评分 5星制 100
Album Rating Computed


Loved              : 标记为喜欢
Persistent ID

Track Type         : 本地 或者 iCloud / Remote / File
Apple Music        : 歌曲可用 ????


Part Of Gapless Album      :    无间隙专辑
Grouping                   :     归类 ?????
Clean                      :     ???? 不知道什么意思

'Protected',
'Location',                : 本地文件地址
'File Folder Count',
'Library Folder Count'
'Normalization',


'Work',                       : 作品名称
'Movement Number',              乐章 1/4
'Movement Count',
'Movement Name',                乐章名称


"""
import datetime
import plistlib
from typing import Any

from objprint import op

from constants import T

FILE = r"C:\Users\10524\Downloads\资料库.xml"


def convert_to_local_time(utc_time: datetime.datetime):
    # local_tz = pytz.timezone('Asia/Shanghai')
    #
    # utc_time = utc_time.replace(tzinfo=pytz.utc)
    # return utc_time.astimezone(local_tz)

    return utc_time + datetime.timedelta(hours=8)


def read_file(filename: str):
    with open(filename, mode='rb') as f:
        data = plistlib.load(f, )

    result_list = []

    attr_name_list = []
    attr_value_list = []
    for attr_name in vars(T):
        if attr_name.startswith('_'):
            continue
        attr_name_list.append(attr_name)
        attr_value_list.append(T.__dict__[attr_name])

    musics = data['Tracks']
    for trac_id, item in musics.items():
        # print(f'start convert track id {trac_id}')
        music_obj = T()

        for idx, attr_name in enumerate(attr_name_list):
            item_value: Any = item.get(attr_value_list[idx])

            if attr_name in ['track_id', 'persistent_id']:
                if item_value is None:
                    raise ValueError('track_id or persistent_id is None')

            # 处理 ，，， &
            # composer 有可能为空
            if attr_name in ['artist', 'album_artist', 'composer']:
                if item_value is None:
                    item_value = ''
                if '&' in item_value:
                    item_value = item_value.replace('&', ',')
                if ',' in item_value:
                    _tmp = item_value.split(',')
                    item_value = ','.join([_s.strip() for _s in _tmp])

            # 处理Bool类型, 如果为None设置为False
            if attr_name in ['explicit', 'compilation', 'apple_music']:
                if item_value is None:
                    item_value = False

            if attr_name == 'year':
                if item_value is None:
                    raise ValueError(f'track id:{trac_id} 的发布日期为空')
            if attr_name == 'release_date':
                if item_value is None:
                    raise ValueError(f'track id:{trac_id} 的发布日期为空')
                item_value = datetime.date(
                    item_value.year,
                    item_value.month,
                    item_value.day,
                )

            if attr_name in ['disc_num', 'disc_cnt', 'track_num', 'track_cnt',
                             'movement_num', 'movement_cnt']:
                if item_value is None:
                    item_value = 0

            if attr_name in ['size', 'total_time', 'bit_rate', 'sample_rate']:
                if item_value is None:
                    item_value = 0

            # UTC 时间 转换为当前时间
            if attr_name in ['date_updated', 'date_added']:
                if item_value is None:
                    raise ValueError(f'track id:{trac_id} 的添加日期或者修改日期为空')
                item_value = convert_to_local_time(item_value)

            if attr_name in ['play_count', 'skip_count']:
                if item_value is None:
                    item_value = 0

            if attr_name in ['play_date', 'skip_date']:
                if item_value is not None:
                    item_value = convert_to_local_time(item_value)

            if attr_name == 'rating':
                if item_value is None:
                    item_value = -1  # -1 意思没有打分
                else:
                    item_value = item_value // 20

            if attr_name in ['loved', 'disliked']:
                if item_value is None:
                    item_value = ''
                else:
                    item_value = '1'
            if attr_name in ['play_date', 'skip_date']:
                if item_value is not None:
                    item_value = convert_to_local_time(item_value)

            if attr_name not in ['play_date', 'skip_date']:
                if item_value is None:
                    # print(f'将 track id:{trac_id} 的字段 {attr_name} 设置为 \'\' ')
                    item_value = ''

            setattr(music_obj, attr_name, item_value)

        op(music_obj)
        result_list.append(music_obj)

    print(f'总共获取了{len(result_list)}个记录')
    return result_list


if __name__ == '__main__':
    read_file(FILE)
