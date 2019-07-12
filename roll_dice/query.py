from roll_dice.result import Result

import numpy as np
import re


simple_query_regex = re.compile(r'(?P<posneg>[\+-])\s*(?P<value>[0-9]+)(?P<d>[dD]?)')

class Query:
    def __init__(self, dice_num: int, bias: int) -> None:
        self._dice_num = dice_num
        self._bias = bias
    
    def roll(self, seed: int = None) -> Result:
        if seed is not None:
            np.random.seed(seed)
        dice = np.random.randint(6, size=self._dice_num) + 1
        return Result(dice=dice, bias=self._bias)

    @staticmethod
    def parse_as_query(text: str) -> 'Query':
        dice_num = 0
        bias = 0
        for match in simple_query_regex.finditer(f'+{text}'):
            direction = int(f'{match.group("posneg")}1')
            value = int(match.group('value'))
            is_dice = (len(match.group('d')) > 0)
            if is_dice:
                dice_num += direction * value
            else:
                bias += direction * value
        if dice_num < 0:
            raise ValueError('Dice num is under zero!')
        return Query(dice_num, bias)
