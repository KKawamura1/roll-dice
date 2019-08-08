import traceback

from roll_dice.colorama import Colorama
from roll_dice.query import Query
from roll_dice.errors import DiceQueryError


def main() -> None:
    # Completion
    import readline

    # Color
    colorama = Colorama()

    while True:
        try:
            line = input('Input: ')
        except EOFError:
            break
        try:
            query, parsed_text = Query.parse_as_query(line, colorama)
        except DiceQueryError:
            print(traceback.format_exc())
            continue
        print(f'Query: {parsed_text}')
        if query.has_dice:
            print(f'Dice: {query}')
            result = query.roll()
            print(f'Result: {result}')
        else:
            print(f'Result: {query}')
        print()


if __name__ == "__main__":
    main()
