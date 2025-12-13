"""
all keys for music contents


"""


class Schema(object):
    pass


class T:
    # db_id
    # db_create_time

    track_id = "Track ID"  # personal track id
    persistent_id = "Persistent ID"  # Persistent ID

    name = "Name"  # 歌曲名称
    artist = "Artist"  # 艺人     , , , &
    album = "Album"  # 专辑
    album_artist = "Album Artist"  # 专辑艺人   &  ,
    composer = "Composer"  # 作曲者    &  ,
    explicit = "Explicit"  # E标
    compilation = "Compilation"  # 专辑是多个艺人的歌曲合辑
    grouping = "Grouping"  # 归类为
    genre = "Genre"  # 歌曲类型

    year = "Year"  # 发行年份
    release_date = "Release Date"  # 发行日期  1986-02-12T12:00:00Z

    disc_num = "Disc Number"  # 光盘编号
    disc_cnt = "Disc Count"
    track_num = "Track Number"  # 音轨
    track_cnt = "Track Count"

    work = "Work"  # 作品名称
    movement_num = "Movement Number"  # 乐章编号 1/4
    movement_cnt = "Movement Count"  # 乐章编号 1/4
    movement_name = "Movement Name"  # 乐章名称

    kind = "Kind"  # 文件类型
    size = "Size"  # 文件大小  Byte
    total_time = "Total Time"  # 文件时长  ms
    bit_rate = "Bit Rate"
    sample_rate = "Sample Rate"
    # track_type = 'Track Type'  # 本地 或者 iCloud / Remote / File
    apple_music = "Apple Music"  # 歌曲可用 ????

    date_updated = "Date Modified"  # 修改日期
    date_added = "Date Added"  # 添加日期 入库时间

    # nullable
    play_count = "Play Count"  # 播放次数
    play_date = "Play Date UTC"  # 上次播放时间
    skip_count = "Skip Count"  # 跳过次数
    skip_date = "Skip Date"  # 上次跳过时间
    rating = "Rating"  # 评分
    loved = "Loved"  # 标记为喜爱
    disliked = "Disliked"  # 标记为不喜爱


if __name__ == "__main__":
    for i in vars(T):
        print(i)
