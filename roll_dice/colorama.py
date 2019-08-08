from colorama import init, deinit


class Colorama:
    def __init__(self) -> None:
        init()

    def __del__(self) -> None:
        deinit()
