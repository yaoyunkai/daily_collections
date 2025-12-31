"""
cards for all

牌组, 等离子牌

增强牌组, 奖励牌，倍率牌，万能牌，玻璃牌，钢铁牌，石头牌，黄金牌，幸运牌。
蜡封 黄红蓝紫
版本 闪箔 镭射 多彩 负片

小丑牌  永恒小丑
优惠券
塔罗牌
星球牌
幻灵牌

small blind
big blind
boss blind

-----------------------------

高牌
对子
两对
三条
顺子
同花
葫芦
四条
同花顺
皇家同花顺
五条
同花葫芦
同花五条

"""

import threading
from enum import StrEnum


class IDGenerator:
    def __init__(self, start=1):
        self._counter = start
        self._lock = threading.Lock()

    def generate_id(self):
        with self._lock:
            id_value = self._counter
            self._counter += 1
            return id_value


class DeckType(StrEnum):
    """
    牌组类型

    """
    RED = 'red_deck'  # 加1弃牌次数
    BLUE = 'blue_deck'  # 加1出牌次数
    YELLOW = 'yellow_deck'  # 游戏开始时拥有额外的10块
    GREEN = 'green_deck'
    BLACK = 'black_deck'
    MAGIC = 'magic_deck'
    NEBULA = 'nebula_deck'
    GHOST = 'ghost_deck'
    ABANDONED = 'abandoned_deck'
    CHECKERED = 'checkered_deck'
    ZODIAC = 'zodiac_deck'
    PAINTED = 'painted_deck'
    ANAGLYPH = 'anaglyph_deck'
    PLASMA = 'plasma_deck'
    ERRATIC = 'erratic_deck'


class EnhancementType(StrEnum):
    """
    增强牌类型

    """
    BONUS = 'bonus_card'
    MULT = 'mult_card'
    WILD = 'wild_card'
    GLASS = 'glass_card'
    STEEL = 'steel_card'
    STONE = 'stone_card'
    GOLD = 'gold_card'
    LUCKY = 'lucky_card'


class EditionType(StrEnum):
    """
    卡牌版本

    """
    BASE = 'base'
    FOIL = 'foil'
    HOLOGRAPHIC = 'holographic'
    POLYCHROME = 'polychrome'
    NEGATIVE = 'negative'


class SealType(StrEnum):
    GOLD = 'gold_seal'
    RED = 'red_seal'
    BLUE = 'blue_seal'
    PURPLE = 'purple_seal'


class StakeType(StrEnum):
    WHITE = 'white_stake'
    RED = 'red_stake'
    GREEN = 'green_stake'
    BLACK = 'black_stake'
    BLUE = 'blue_stake'
    PURPLE = 'purple_stake'
    ORANGE = 'orange_stake'
    GOLD = 'gold_stake'


class SuitType(StrEnum):
    Spade = 'Spade'
    Heart = 'Heart'
    Club = 'Club'
    Diamond = 'Diamond'


class BaseObject:

    def on_play_hand(self, game, ):
        pass

    def on_discard(self, game, ):
        pass

    def on_select_blind(self, game, ):
        pass

    def on_skip_blind(self, game, ):
        pass


class Joker:
    pass


class Card:
    _id: int
    name: str  # 2 - 10 Jack Queen King Ace
    suit: str  # Spade Heart Club Diamond
    nominal: int  # 2-10 10 10 10 11
    extra_nominal: int  # 额外的筹码数
    enhancement: EnhancementType  # 增强牌类型
    edition: EditionType  # 版本
    seal: SealType  # 蜡封类型

    def __str__(self):
        return '{} of {}'.format(self.name, self.suit)


class StoreCard:
    """
    优惠卷
    小丑牌
    星球牌
    幻灵牌
    塔罗牌


    """
    pass


class GameInstance:
    """
    本回合打出过的牌。


    """
    current_round: int
    cnt_round_skipped: int
    current_amount: int
    current_ante: int

    deck_type: DeckType
    stake: StakeType

    deck_cards: list
    vouchers: list  # 已购买优惠券
    jokers: list[Joker]
    num_joker: int

    def init_game(self):
        self.current_round = 0
        self.deck_type = DeckType.PLASMA
        self.deck_cards = []
        self.jokers = []
        self.num_joker = 5


if __name__ == '__main__':
    obj = Card()
    obj.name = '5'
    obj.suit = SuitType.Diamond
    print(obj)
