import sys

from src.bot import create_app


def main() -> int:
    try:
        app = create_app()
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