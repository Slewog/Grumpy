import sys

from src import create_bot


def main() -> int:
    try:
        app = create_bot()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        app.run()
    except KeyboardInterrupt:
        return 130

    return 0

if __name__ == "__main__":
    raise SystemExit(main())