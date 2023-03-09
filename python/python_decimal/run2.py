"""


Created at 2023/3/9
"""

import decimal

decimal.getcontext().prec = 4
decimal.getcontext().rounding = decimal.ROUND_HALF_UP

TWOPLACES = decimal.Decimal('0.01')


def test_compute_tax():
    price = decimal.Decimal('19.99')

    tax_rate = decimal.Decimal('0.08')

    tax = price * tax_rate

    total_price = price + tax

    total_price = total_price.quantize(TWOPLACES)

    # 输出结果
    print('Price: ${}'.format(price))
    print('Tax rate: {}'.format(tax_rate))
    print('Tax: ${}'.format(tax))
    print('Total price: ${}'.format(total_price))


def test_unit():
    total = decimal.Decimal('10.01')
    unit = total / 3
    unit = unit.quantize(TWOPLACES)
    print(f'unit price is {unit}')


if __name__ == '__main__':
    test_compute_tax()
    test_unit()
