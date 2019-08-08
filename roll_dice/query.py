from typing import Mapping, Optional, Tuple
import re
from collections import defaultdict
import numpy as np
from colorama import Fore

from roll_dice.colorama import Colorama
from roll_dice.result import Result
from roll_dice.errors import DiceQueryError


simple_query_regex = re.compile(
    r'(?P<posneg>[\+-])?\s*(?P<value>[0-9]+)?(?P<d>[dD])?(?P<dice_kind>[0-9]+)?'
)


def str_to_int_with_default(target: Optional[str], default: int) -> int:
    if target is None:
        return default
    return int(target)


class Query:
    def __init__(
            self,
            dice_num_map: Mapping[int, int],
            bias: int,
    ) -> None:
        self._dice_num_map = dice_num_map
        self._bias = bias

    @property
    def has_dice(self) -> bool:
        return len(self._dice_num_map) > 0

    def roll(self, seed: int = None) -> Result:
        if seed is not None:
            np.random.seed(seed)
        dice_map = {
            dice_kind: list(np.random.randint(dice_kind, size=dice_num) + 1)
            for dice_kind, dice_num in self._dice_num_map.items()
        }
        return Result(dice_map=dice_map, bias=self._bias)

    def __str__(self) -> str:
        dice_num_list = sorted(
            [
                (dice_kind, dice_num)
                for dice_kind, dice_num in self._dice_num_map.items()
            ]
        )
        dice_num_str_list = [
            f"{dice_num}d{dice_kind}"
            for dice_kind, dice_num in dice_num_list
        ]
        if not(self._bias == 0 and len(dice_num_str_list) > 0):
            dice_num_str_list.append(str(self._bias))
        return ' + '.join(dice_num_str_list)

    @staticmethod
    def parse_as_query(
            text: str,
            colorama: Optional[Colorama] = None
    ) -> Tuple['Query', str]:
        # Parse text
        dice_num_map = defaultdict(int)
        bias = 0
        parsed_positions = []
        for match in simple_query_regex.finditer(text):
            posneg = match.group('posneg')
            if posneg is None:
                direction = 1
            else:
                direction = int(f'{posneg}1')
            is_dice = (match.group('d') is not None)
            if is_dice:
                value = str_to_int_with_default(match.group('value'), default=1)
                kind = str_to_int_with_default(match.group('dice_kind'), default=6)
                dice_num_map[kind] += direction * value
            else:
                value_str = match.group('value')
                if value_str is None:
                    continue
                value = int(value_str)
                bias += direction * value
            parsed_positions.append((match.start(), match.end(), is_dice))

        # Generate colored text
        if colorama is not None:
            parsed_positions = sorted(parsed_positions)
            result_text = f''
            last_pos = 0
            for begin, end, is_dice in parsed_positions:
                result_text += text[last_pos:begin]
                if is_dice:
                    color = Fore.LIGHTBLUE_EX
                else:
                    color = Fore.GREEN
                result_text += f'{color}{text[begin:end]}{Fore.RESET}'
                last_pos = end
            result_text += text[last_pos:]
        else:
            result_text = text

        # Sanity check
        if any([dice_num <= 0 for dice_kind, dice_num in dice_num_map.items()]):
            raise DiceQueryError('The number of dice cannot be zero!')
        if any([dice_kind <= 0 for dice_kind, dice_num in dice_num_map.items()]):
            raise DiceQueryError('The size of die cannot be zero!')

        return Query(dice_num_map, bias), result_text
