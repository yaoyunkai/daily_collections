"""

计算牌型


高牌 high card
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

=============================================
四指: 同花和顺子可以由四张牌构成
幻视: 所有卡牌视为人头牌。 和 学者 互动吗？
学者: 打出的A在计分时加4倍和20筹码
捷径: 让顺子可以相隔一个点数组成。优先级不如对子？
模糊小丑: 红桃和方块视为一个花色 黑桃和梅花视为一个花色。


万能牌  wild card
石头牌  stone card  不影响牌型计算。

最多打出五张牌

created at 2025/4/17
"""

from enum import StrEnum
from typing import Optional

from utils import _print_noun

CHIP_MAPPING = {
    'A': 11,
    'J': 10,
    'Q': 10,
    'K': 10,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

_unset = object()


class SuitType(StrEnum):
    Spade = 'spade'
    Heart = 'heart'
    Club = 'club'
    Diamond = 'diamond'


class EnhancedType(StrEnum):
    """
    增强牌类型

    """
    StoneCard = 'Stone'
    WildCard = 'Wild'


class Card:
    """


    suit:
        Spade    黑桃
        Heart    红桃
        Club     梅花
        Diamond  方块

    type:
        数字牌，人头牌，A
        Aces
        Face Cards
        Numbered Cards

    enhanced cards
        stone card
        wild card

    """

    def __init__(self, number: str, suit: SuitType, enhanced_type: Optional[EnhancedType] = None):
        if number not in CHIP_MAPPING:
            raise ValueError('invalid number')
        self.number = number
        self.suit = suit
        self.enhanced_type = enhanced_type

    def __str__(self):
        if self.enhanced_type:
            _prefix = '{} Card'.format(self.enhanced_type)
        else:
            _prefix = 'Card'

        return f'{_prefix} <{self.suit} of {self.number}>'


class Application:
    def __init__(self):
        self.jokers = []
        self.joker_slot = 5
        self.current_play_cards = []

    def compute_poker_hands(self, played_cards: list[Card]):
        print(f'choices {_print_noun("card", len(played_cards))} for start play')
        self.current_play_cards = played_cards

    def _is_flush_five(self):
        """
        同花五条

        """
        if len(self.current_play_cards) < 5:
            return False
        return None


if __name__ == '__main__':
    c1 = Card('K', SuitType.Heart, EnhancedType.WildCard)
    c2 = Card('K', SuitType.Diamond)

    app = Application()
    app.compute_poker_hands([c1, c2])
