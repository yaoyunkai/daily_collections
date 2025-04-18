"""


created at 2025/4/18
"""

def _print_noun(noun_val: str, numbers: int):
    if numbers > 1:
        noun_val = '{}s'.format(noun_val)
    return f'{numbers} {noun_val}'
