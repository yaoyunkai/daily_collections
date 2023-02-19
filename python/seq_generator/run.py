"""
序列号生成


Create at 2023/2/18 22:10
"""
import re


class SerialNumberGenerator:
    """
    前提条件: 序列是从零开始

    """
    SEQ_ITEMS = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    SEQ_ITEMS_PATTERN = re.compile(r'^[0123456789ABCDEFGHJKLMNPQRSTUVWXYZ]+$')

    @classmethod
    def convert_to_sequence(cls, number: int):
        """
        将数字转换为序列

        :param number:
        :return:
        """
        if number < 0:
            raise ValueError('numbers must be >= 0')

        _sequence_arr = []

        while True:
            lts, rts = divmod(number, len(cls.SEQ_ITEMS))
            _sequence_arr.append(cls.SEQ_ITEMS[rts])
            if lts == 0:
                break
            number = lts
        _sequence_arr.reverse()
        return ''.join(_sequence_arr)

    @classmethod
    def convert_to_numbers(cls, sequence_string: str):
        """
        将序列转换为数字

        :param sequence_string:
        :return:
        """
        if not cls.SEQ_ITEMS_PATTERN.match(sequence_string):
            raise ValueError('sequence string is not formatted')

        _number = 0
        seq_str = sequence_string[::-1]
        for idx, ch in enumerate(seq_str):
            num = (len(cls.SEQ_ITEMS) ** idx) * cls.SEQ_ITEMS.find(ch)
            _number = _number + num
        return _number


class ExcelColumnGenerator:
    # A == 1  z == 26
    EXCEL_SEQ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    EXCEL_SEQ_PATTERN = re.compile(r'^[A-Z]+$')

    @classmethod
    def excel_title_to_number(cls, sequence: str):
        if not cls.EXCEL_SEQ_PATTERN.match(sequence):
            raise ValueError('sequence is not formatted')
        _number = 0
        seq_str = sequence[::-1]
        for idx, ch in enumerate(seq_str):
            _number += (len(cls.EXCEL_SEQ) ** idx) * (cls.EXCEL_SEQ.find(ch) + 1)
        return _number

    @classmethod
    def excel_number_to_title(cls, number: int):
        if number <= 0:
            raise ValueError('number must be >= 0')
        _sequence_arr = []
        while number > 0:
            # 由于进制从1开始，所以减一后取模再把数字补1
            a0 = (number - 1) % len(cls.EXCEL_SEQ) + 1
            _sequence_arr.append(cls.EXCEL_SEQ[a0 - 1])
            number = (number - a0) // len(cls.EXCEL_SEQ)
        _sequence_arr.reverse()
        return ''.join(_sequence_arr)


if __name__ == '__main__':
    # for i in range(100000000, 100000000 + 500):
    #     _ret = SerialNumberGenerator.convert_to_sequence(i)
    #     _num = SerialNumberGenerator.convert_to_numbers(_ret)
    #
    #     print('{} - {} - {}'.format(i, _ret, _num))
    print(SerialNumberGenerator.convert_to_numbers('ZZZZ'))
    print(SerialNumberGenerator.convert_to_sequence(1336335))

    print(ExcelColumnGenerator.excel_title_to_number('AAZ'))
    print(ExcelColumnGenerator.excel_number_to_title(728))

    print(ExcelColumnGenerator.excel_title_to_number('AASR'))
    print(ExcelColumnGenerator.excel_number_to_title(1))
