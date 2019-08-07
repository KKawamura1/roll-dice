import traceback

from roll_dice.query import Query
from roll_dice.errors import DiceQueryError


def main() -> None:
    # Completion
    import readline

    while True:
        try:
            line = input('Input: ')
        except EOFError:
            break
        try:
            result = Query.parse_as_query(line).roll()
        except DiceQueryError:
            print(traceback.format_exc())
            continue
        print(str(result))


if __name__ == "__main__":
    main()
