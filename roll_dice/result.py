from typing import Sequence


class Result:
    def __init__(self, dice: Sequence[int], bias: int) -> None:
        dice = sorted(list(dice), reverse=True)
        self.dice = dice
        self.bias = bias

        dice_num = len(dice)
        self.critical = (dice_num >= 2 and dice[1] == 6)
        self.fumble = (dice_num == 0 or all([die == 1 for die in dice]))
        self.sum_value = sum(dice) + bias
    
    def __str__(self) -> str:
        critical_str = '(Critical!) ' if self.critical else ''
        fumble_str = '(Fumble!) ' if self.fumble else ''
        return f'Result: {self.sum_value} {critical_str}{fumble_str}({str(self.dice)} + {self.bias})'
