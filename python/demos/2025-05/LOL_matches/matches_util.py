"""


created at 2025/5/4
"""
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil import parser
from sqlalchemy import BigInteger, Boolean, Integer, String, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass


class NewMatch(Base):
    __tablename__ = "new_matches"

    # 主键和字段
    game_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="比赛唯一ID")
    game_start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False,
        comment="比赛开始时间（不含时区）"
    )
    game_duration: Mapped[int] = mapped_column(Integer, nullable=False, comment="比赛持续时间（秒）")
    queue_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="队列ID（如排位赛、匹配赛等）")
    game_end_result: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="",
        server_default=text(''),
        comment="游戏结束时的状态"
    )

    participants: Mapped[list["NewParticipant"]] = relationship(back_populates='match', cascade='all, delete-orphan')

    # 表注释
    __table_args__ = {"comment": "比赛记录"}


class NewParticipant(Base):
    __tablename__ = "new_participants"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="参与者唯一ID")

    # 参与者位置索引
    participant_idx: Mapped[int] = mapped_column(Integer, nullable=False, comment="召唤师位置索引（1-10）")

    # 外键关联比赛ID
    game_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(NewMatch.game_id),
        nullable=False,
        comment="关联的比赛ID"
    )

    # 基础信息
    summoner_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="召唤师唯一ID")
    nick: Mapped[str] = mapped_column(String(100), nullable=False, comment="召唤师昵称")
    team_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="队伍ID")
    champion_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="使用的英雄ID")

    # 技能ID
    spell0_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="召唤师技能1")
    spell1_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="召唤师技能2")

    # 战斗结果
    win: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="是否胜利")

    # 装备ID（0-6）
    item0_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏0")
    item1_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏1")
    item2_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏2")
    item3_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏3")
    item4_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏4")
    item5_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏5")
    item6_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="装备栏6")

    # 符文ID
    perk0_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="主系符文")
    perk1_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="副系符文")

    # 战斗数据
    kills: Mapped[int] = mapped_column(Integer, nullable=False, comment="击杀数")
    deaths: Mapped[int] = mapped_column(Integer, nullable=False, comment="死亡数")
    assists: Mapped[int] = mapped_column(Integer, nullable=False, comment="助攻数")
    gold_earned: Mapped[int] = mapped_column(Integer, nullable=False, comment="获得金钱")
    damage_dtc: Mapped[int] = mapped_column(Integer, nullable=False, comment="对英雄造成的伤害")
    damage_total: Mapped[int] = mapped_column(Integer, nullable=False, comment="总伤害输出")
    damage_taken: Mapped[int] = mapped_column(Integer, nullable=False, comment="承受总伤害")

    match: Mapped['NewMatch'] = relationship(back_populates='participants', )

    # 表注释
    __table_args__ = {"comment": "比赛参与者数据"}


def _get_datetime(val: str):
    dt = parser.isoparse(val)
    dt_local = dt.astimezone(ZoneInfo('Asia/Shanghai'))
    return dt_local


class SQLHelper:
    def __init__(self):
        self.engine = create_engine("postgresql://user1:user1@localhost/lol_match_records", echo=True)
        self.game_id_list = None
        self.session = None

    def load_matches_from_file(self, dir_path):
        if not os.path.exists(dir_path) and not os.path.isdir(dir_path):
            print(f'路径不存在，{dir_path}')
            return

        self.get_game_id_list()
        self.session = Session(self.engine)

        for _path in os.listdir(dir_path):
            if not _path.endswith('.json'):
                continue

            with open(os.path.join(dir_path, _path), encoding='utf8') as fp:
                row_data = json.load(fp)
                row_data = row_data['games']['games']
                for one_record in row_data:
                    print(f'开始处理id为 {one_record["gameId"]} 游戏类型为 {one_record["queueId"]} 的比赛数据')
                    if one_record['queueId'] != 450:
                        continue
                    try:
                        self._convert_to_object(one_record)
                    except Exception as e:
                        print(f'转换数据遇到错误: {e}')

        self.session.commit()
        self.session = None

    def get_game_id_list(self):
        with Session(self.engine) as session:
            # 构造查询语句：SELECT game_id FROM new_matches
            stmt = select(NewMatch.game_id)

            # 执行查询并提取所有 game_id（返回类型为 List[int]）
            game_ids = session.scalars(stmt).all()
            self.game_id_list = game_ids
            print(f'game id list is: {self.game_id_list}')

    def _convert_to_object(self, one_record: dict):
        game_id = one_record['gameId']

        if game_id in self.game_id_list:
            print(f'game id: {game_id} 已经存在, skipped')
            return
        self.game_id_list.append(game_id)

        game_start_time = _get_datetime(one_record['gameCreationDate'])
        game_duration = one_record['gameDuration']
        queue_id = one_record['queueId']
        game_end_result = one_record['gameDetail'].get('endOfGameResult', '')

        obj_match = NewMatch(
            game_id=game_id,
            game_start_time=game_start_time,
            game_duration=game_duration,
            queue_id=queue_id,
            game_end_result=game_end_result,
        )
        self.session.add(obj_match)

        participant_identities = one_record['gameDetail']['participantIdentities']
        participants = one_record['gameDetail']['participants']

        if len(participant_identities) != len(participants):
            raise ValueError('data length mismatch')
        if len(participant_identities) != 10:
            raise ValueError('require 10')

        for idx, participant_item in enumerate(participants):
            player_info = participant_identities[idx]
            player_info = player_info['player']

            summoner_id = player_info['summonerId']
            nick = f'{player_info["gameName"]}#{player_info["tagLine"]}'

            participant_idx = participant_item['participantId']
            team_id = participant_item['teamId']
            champion_id = participant_item['championId']

            spell0_id = participant_item.get('spell1Id', 0)
            spell1_id = participant_item.get('spell2Id', 0)

            win = participant_item['stats']['win']
            item_list = [participant_item['stats'].get(f'item{_i}', 0) for _i in range(7)]

            perk_list = [participant_item['stats'].get('perkPrimaryStyle', 0),
                         participant_item['stats'].get('perkSubStyle', 0)]

            k = participant_item['stats']['kills']
            d = participant_item['stats']['deaths']
            a = participant_item['stats']['assists']
            gold_earned = participant_item['stats']['goldEarned']
            damage_dtc = participant_item['stats']['totalDamageDealtToChampions']
            damage_total = participant_item['stats']['totalDamageDealt']
            damage_taken = participant_item['stats']['totalDamageTaken']

            obj_part = NewParticipant(
                participant_idx=participant_idx,
                summoner_id=summoner_id,
                nick=nick,
                team_id=team_id,
                champion_id=champion_id,
                spell0_id=spell0_id,
                spell1_id=spell1_id,
                win=win,
                item0_id=item_list[0],
                item1_id=item_list[1],
                item2_id=item_list[2],
                item3_id=item_list[3],
                item4_id=item_list[4],
                item5_id=item_list[5],
                item6_id=item_list[6],
                perk0_id=perk_list[0],
                perk1_id=perk_list[1],
                kills=k, deaths=d, assists=a,
                gold_earned=gold_earned,
                damage_dtc=damage_dtc,
                damage_total=damage_total,
                damage_taken=damage_taken,
            )
            obj_match.participants.append(obj_part)


if __name__ == '__main__':
    app = SQLHelper()
