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
from enum import StrEnum, unique

from utils import IdGenerator, print_noun

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


@unique
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


@unique
class SuitType(StrEnum):
    """
    继承自 str，成员值自动转换为字符串 。

    """
    Spade = 'spade'  # 黑桃
    Heart = 'heart'  # 红桃
    Club = 'club'  # 梅花
    Diamond = 'diamond'  # 方片


@unique
class EnhancedType(StrEnum):
    """
    增强牌类型

    """
    Null = 'null'  # 没有增强类型
    StoneCard = 'Stone'  # 石头牌，50筹码 打出时总是计分
    WildCard = 'Wild'  # 万能牌
    BonusCard = 'Bonus'  # 奖励牌，加三十额外筹码
    MultCard = 'Mult'  # 倍率牌，加4倍率
    GlassCard = 'Glass'  # 玻璃牌，x2 倍率， 四分之一的机率摧毁这张牌
    SteelCard = 'Steel'  # 留在手牌时 x1.5倍率
    GoldCard = 'Gold'  # 黄金牌， 如果这张牌在回合结束时还在手里，就得 3 块
    LuckyCard = 'Lucky'  # 幸运牌, 1/5 的几率获得+20 倍率，1/15 的机率赢得 20 块


class Card:
    """
    游戏牌

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

    def __init__(self, rank: str, suit: SuitType, enhanced_type: EnhancedType = EnhancedType.Null):
        if rank not in CHIP_MAPPING:
            raise ValueError('invalid number')
        self.rank = rank  # 2 - A
        self.suit = suit  # 花色
        self.enhanced_type = enhanced_type  # 增强牌类型
        self.chips = CHIP_MAPPING[self.rank]  # 可以被小丑牌增加

        self._id = IdGenerator.get_next_id()

    def __str__(self):
        if self.enhanced_type is not EnhancedType.Null:
            _prefix = '{} Card'.format(self.enhanced_type)
        else:
            _prefix = 'Card'

        return f'{_prefix}-{self._id} <{self.suit} of {self.rank}>'

    def __repr__(self):
        return self.__str__()


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

        # non-permanent variables
        self.cur_play_cards = []  # 当前打出的牌
        self.cur_has_flush = False  # 当前是否包含同花
        self.cur_flush_cards = []  # 当前的同花牌

    def on_joker_changed(self):
        """
        每次有小丑牌变化时，调用这个方法

        """
        pass

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

        print(f'choices {print_noun("card", len(played_cards))} for start play')
        self.cur_play_cards = played_cards

        self._check_flush()
        print(f'has flush: {self.cur_has_flush}')
        print(f'flush: {self.cur_flush_cards}')

    def _check_flush(self):
        """
        判断是否符合同花规则, 如下小丑和增强牌对判断有影响

        cur_has_flush
        cur_flush_cards

        模糊小丑,
        四指,
        万能牌,

        """

        suit_bit_map = {
            SuitType.Spade: 0,
            SuitType.Heart: 1,
            SuitType.Club: 2,
            SuitType.Diamond: 3,
        }

        if len(self.cur_play_cards) < 4:
            self.cur_has_flush = False
            return

        # 黑 红 梅 方
        flush_list = [[], [], [], []]

        for card in self.cur_play_cards:
            if card.enhanced_type is EnhancedType.StoneCard:
                continue

            if card.enhanced_type is EnhancedType.WildCard:
                flush_list[0].append(card)
                flush_list[1].append(card)
                flush_list[2].append(card)
                flush_list[3].append(card)
                continue

            # 模糊小丑
            if self.flag_joker_smeared_joker:
                if card.suit is SuitType.Spade or card.suit is SuitType.Club:
                    flush_list[0].append(card)
                    flush_list[2].append(card)
                else:
                    flush_list[1].append(card)
                    flush_list[3].append(card)

            else:
                flush_list[suit_bit_map[card.suit]].append(card)

        flush_cards = []

        for flush in flush_list:
            if len(flush) > len(flush_cards):
                flush_cards = flush

        minimum_length = 5 if not self.flag_joker_four_fingers else 4
        if len(flush_cards) >= minimum_length:
            self.cur_has_flush = True
            self.cur_flush_cards = flush_cards
        else:
            self.cur_has_flush = False
            self.cur_flush_cards = []


if __name__ == '__main__':
    c1 = Card('K', SuitType.Heart, EnhancedType.WildCard)
    c2 = Card('5', SuitType.Club)
    c3 = Card('7', SuitType.Club)
    c4 = Card('3', SuitType.Club)
    c5 = Card('2', SuitType.Spade)

    app = Application()
    app.set_deck_type(DeckType.PlasmaDeck)
    app.flag_joker_smeared_joker = True
    app.flag_joker_four_fingers = False
    app.compute_poker_hands([c1, c2, c3, c4, c5])
