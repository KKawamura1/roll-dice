from typing import Mapping, Optional
import re
from collections import defaultdict
import numpy as np

from roll_dice.result import Result
from roll_dice.errors import DiceQueryError


simple_query_regex = re.compile(
    r'(?P<posneg>[\+-])\s*(?P<value>[0-9]+)?(?P<d>[dD])?(?P<dice_kind>[0-9]+)?'
)


def str_to_int_with_default(target: Optional[str], default: int) -> int:
    if target is None:
        return default
    return int(target)


class Query:
    def __init__(self, dice_num_map: Mapping[int, int], bias: int) -> None:
        self._dice_num_map = dice_num_map
        self._bias = bias

    def roll(self, seed: int = None) -> Result:
        if seed is not None:
            np.random.seed(seed)
        dice_map = {
            dice_kind: list(np.random.randint(dice_kind, size=dice_num) + 1)
            for dice_kind, dice_num in self._dice_num_map.items()
        }
        return Result(dice_map=dice_map, bias=self._bias)

    @staticmethod
    def parse_as_query(text: str) -> 'Query':
        dice_num_map = defaultdict(int)
        bias = 0
        for match in simple_query_regex.finditer(f'+{text}'):
            direction = int(f'{match.group("posneg")}1')
            is_dice = (match.group('d') is not None)
            if is_dice:
                value = str_to_int_with_default(match.group('value'), default=1)
                kind = str_to_int_with_default(match.group('dice_kind'), default=6)
                dice_num_map[kind] += direction * value
            else:
                value = str_to_int_with_default(match.group('value'), default=0)
                bias += direction * value
        if any([dice_num <= 0 for dice_kind, dice_num in dice_num_map.items()]):
            raise DiceQueryError('The number of dice cannot be zero!')
        if any([dice_kind <= 0 for dice_kind, dice_num in dice_num_map.items()]):
            raise DiceQueryError('The size of die cannot be zero!')

        return Query(dice_num_map, bias)
