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
            query = Query.parse_as_query(line)
        except DiceQueryError:
            print(traceback.format_exc())
            continue
        print(f'Query: {query}')
        result = query.roll()
        print(f'Result: {result}')
        print()


if __name__ == "__main__":
    main()
