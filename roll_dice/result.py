from typing import Sequence, Mapping


class Result:
    def __init__(self, dice_map: Mapping[int, Sequence[int]], bias: int) -> None:
        dice_list = sorted(
            [
                (dice_kind, sorted(list(dice), reverse=True))
                for dice_kind, dice in dice_map.items()
            ],
            reverse=False
        )
        self.dice_list = dice_list
        self.bias = bias

    def __str__(self) -> str:
        if len(self.dice_list) == 0:
            result = str(self.bias)
        elif len(self.dice_list) == 1:
            dice_kind, dice = self.dice_list[0]
            dice_num = len(dice)
            if dice_kind == 6:
                critical = (dice_num >= 2 and dice[1] == 6)
                fumble = all([die == 1 for die in dice])
            elif dice_kind == 100 and dice_num == 1:
                critical = (1 <= dice[0] <= 5)
                fumble = (96 <= dice[0] <= 100)
            else:
                critical = fumble = False
            sum_value = sum(dice) + self.bias
            critical_str = '(Critical!) ' if critical else ''
            fumble_str = '(Fumble!) ' if fumble else ''
            bias_str = f' + {self.bias}' if self.bias != 0 else ''
            result = f'{sum_value} {critical_str}{fumble_str}({str(dice)}{bias_str})'
        else:
            sum_value = sum([sum(dice) for dice_kind, dice in self.dice_list])
            result_for_each_kind = [
                f'({len(dice)}d{dice_kind}: {str(dice)})'
                for dice_kind, dice in self.dice_list
            ]
            if self.bias != 0:
                result_for_each_kind.append(f'(bias: {self.bias})')
            result = f'{sum_value} {" ".join(result_for_each_kind)}'
        return result
