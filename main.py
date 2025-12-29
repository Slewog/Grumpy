import sys

def main() -> int:
    try:
        # Your main application logic here
        print("App creation")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        print("App would be run.")
    except KeyboardInterrupt:
        return 130

    return 0

if __name__ == "__main__":
    raise SystemExit(main())