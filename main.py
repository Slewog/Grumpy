import sys

from src.bot import create_bot

INPUT_MSG = "GRUMPY - Press Enter to close the program"

def print_error(exc: str):
    print(exc, file=sys.stderr)
    input(INPUT_MSG)


def main() -> int:
    try:
        app = create_bot()
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print_error(str(exc))
        return 1

    try:
        app.run()
    except KeyboardInterrupt:
        return 130
    except FileNotFoundError as exc:
        print_error(str(exc))
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())