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
哪些小丑牌会影响牌型计算呢？

    增强牌组: 石头牌，万能牌
    小丑:


四指: 同花和顺子可以由四张牌构成
幻视: 所有卡牌视为人头牌。 和 学者 互动吗？
学者: 打出的A在计分时加4倍和20筹码
捷径: 让顺子可以相隔一个点数组成。优先级不如对子？
模糊小丑: 红桃和方块视为一个花色 黑桃和梅花视为一个花色。
哑剧演员: 重新触发留在手牌中的牌的能力
飞溅: 每张打出的牌都可以计分。
吸血鬼: 每打出一张计分的增加牌组，这张小丑牌获得0.1 倍率，并移除卡牌的增强效果。
喜与悲: 重新触发所有打出的人头牌。


万能牌  wild card
石头牌  stone card  不影响牌型计算。

最多打出五张牌


on_start ->
on_compute ->


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


class DeckType(StrEnum):
    RedDeck = 'red_deck'  # 加一弃牌次数
    BlueDeck = 'blue_deck'  # 加一出牌次数
    YellowDeck = 'yellow_deck'  # 开局获得额外的10块
    GreenDeck = 'green_deck'  # Round 回合结束时，每个剩余出牌 2块钱， 每个剩余弃牌 1块钱，不赚取任何利息
    BlackDeck = 'black_deck'
    MagicDeck = 'magic_deck'
    NebulaDeck = 'nebula_deck'
    GhostDeck = 'ghost_deck'
    AbandonedDeck = 'abandoned_deck'
    CheckeredDeck = 'checkered_deck'
    ZodiacDeck = 'zodiac_deck'
    PaintedDeck = 'painted_deck'
    AnaglyphDeck = 'anaglyph_deck'
    PlasmaDeck = 'plasma_deck'
    ErraticDeck = 'erratic_deck'


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
    额外的位置记录 筹码

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
    # 拥有某个小丑的标志位
    flag_joker_smeared_joker = False  # 模糊小丑
    flag_joker_four_fingers = False  # 四指
    flag_joker_shortcut = False  # 捷径
    flag_joker_splash = False  # 飞溅
    flag_joker_pareidolia = False  # 幻视

    def __init__(self):
        self.deck_type = None  # 牌组类型, 可能对计分方式有影响
        self.jokers = []
        self.joker_slot = 5  # 当前总共的小丑栏位
        self.current_play_cards = []

    def _compute_joker_flags(self):
        for attr_name in self.__class__.__dict__:
            if attr_name.startswith('flag_joker_'):
                setattr(self, attr_name, False)

    def set_deck_type(self, deck_type: DeckType):
        if self.deck_type:
            print(f'already set deck type as {self.deck_type}, can\'t set again')
            return

        self.deck_type = deck_type
        if self.deck_type is DeckType.BlackDeck:
            self.joker_slot = 6

    def compute_poker_hands(self, played_cards: list[Card]):
        if not self.deck_type:
            raise SystemError('can\'t play without deck type')

        print(f'choices {_print_noun("card", len(played_cards))} for start play')
        self.current_play_cards = played_cards

    def _is_flush_five(self):
        """
        同花五条

        """
        if len(self.current_play_cards) < 5:
            return False

        first = self.current_play_cards[0]

        return None


if __name__ == '__main__':
    c1 = Card('K', SuitType.Heart, EnhancedType.WildCard)
    c2 = Card('K', SuitType.Diamond)

    app = Application()
    app.set_deck_type(DeckType.PlasmaDeck)
    app.compute_poker_hands([c1, c2])
