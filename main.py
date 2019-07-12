import argparse
from roll_dice.query import Query


def main(arg: str = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    if arg is not None:
        params = parser.parse_args(arg.split())
    else:
        params = parser.parse_args()
    target: str = params.target
    print(target)
    result = Query.parse_as_query(target).roll()
    print(str(result))


if __name__ == "__main__":
    main()
