from roll_dice.query import Query


def main() -> None:
    # Completion
    import readline

    while True:
        try:
            line = input('Input: ')
        except EOFError:
            break
        result = Query.parse_as_query(line).roll()
        print(str(result))


if __name__ == "__main__":
    main()
