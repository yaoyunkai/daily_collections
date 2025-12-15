"""
all keys for music contents

Keys from file: Tracks / Playlists

Keys:  Podcast / Apple Music
Track Type: Remote / URL

-------------------------------------------------

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
from functools import lru_cache

KEY_LIST = [
    'Track ID',
    'Name',
    'Artist',
    'Album Artist',
    'Composer',
    'Album',
    'Genre',
    'Kind',  # need check
    'Size',
    'Total Time',
    'Disc Number',
    'Disc Count',
    'Track Number',
    'Track Count',
    'Year',
    'Date Modified',
    'Date Added',
    'Bit Rate',
    'Sample Rate',
    'Play Count',
    'Play Date',
    'Play Date UTC',
    'Skip Count',
    'Skip Date',
    'Release Date',
    'Compilation',
    'Artwork Count',  # need check

    'Sort Album',
    'Sort Artist',
    'Sort Album Artist',
    'Sort Name',
    'Sort Composer',

    'Persistent ID',
    'Track Type',  # need check
    'Apple Music',  # flag
    'Loved',
    'Part Of Gapless Album',
    'Rating',
    'Album Rating',
    'Album Rating Computed',
    'Grouping',  # 古典音乐才有
    'Explicit',  # E标
    'Work',
    'Movement Number',
    'Movement Count',
    'Movement Name',
    'Normalization',  # 下载到本地的才有
    'Protected',  # 下载到本地的才有
    'Location',  # 本地文件路径
    'File Folder Count',  # 下载到本地的才有
    'Library Folder Count',  # 下载到本地的才有
    'Clean',  # 歌曲是否有部分片段被清除 ???
    'Podcast',  # 博客
    'Unplayed',  # 博客项目才有
    'Playlist Only'  # 只在播放列表，不在资料库的。
]


class Schema:
    """
    歌曲属性字段
    个人数据字段

    """
    track_id = 'Track ID'  # personal track id
    persistent_id = "Persistent ID"  # Persistent ID

    kind = 'Kind'  # ???
    artwork_count = 'Artwork Count'
    track_type = 'Track Type'

    # 歌曲属性字段
    name = "Name"  # 歌曲名称
    artist = "Artist"  # 艺人     , , , &
    album = "Album"  # 专辑
    album_artist = "Album Artist"  # 专辑艺人   &  ,
    composer = "Composer"  # 作曲者    &  ,
    genre = "Genre"  # 歌曲类型
    explicit = "Explicit"  # E标
    clean = 'Clean'  # 歌曲是否有部分片段被清除 ???
    compilation = "Compilation"  # 专辑是多个艺人的歌曲合辑

    size = 'Size'  # 文件大小 Byte
    total_time = "Total Time"  # 文件时长  ms
    bit_rate = "Bit Rate"
    sample_rate = "Sample Rate"
    disc_num = "Disc Number"  # 光盘编号
    disc_cnt = "Disc Count"
    track_num = "Track Number"  # 音轨
    track_cnt = "Track Count"
    year = "Year"  # 发行年份
    release_date = "Release Date"  # 发行日期  1986-02-12T12:00:00Z
    # 古典信息字段
    work = "Work"  # 作品名称
    grouping = "Grouping"  # 归类为
    movement_num = "Movement Number"  # 乐章编号 1/4
    movement_cnt = "Movement Count"  # 乐章编号 1/4
    movement_name = "Movement Name"  # 乐章名称

    # 个人信息字段
    date_added = "Date Added"  # 添加日期 入库时间
    date_updated = "Date Modified"  # 修改日期
    play_count = "Play Count"  # 播放次数
    play_date = "Play Date UTC"  # 上次播放时间
    skip_count = "Skip Count"  # 跳过次数
    skip_date = "Skip Date"  # 上次跳过时间

    rating = "Rating"  # 评分
    album_rating = 'Album Rating'  # 专辑评分
    loved = "Loved"  # 标记为喜爱


@lru_cache
def get_schema_dict():
    new_dict = {}
    for k, v in Schema.__dict__.items():
        if k.startswith('_'):
            continue
        new_dict[k] = v
    return new_dict


if __name__ == '__main__':
    result = get_schema_dict()
    print(result)
