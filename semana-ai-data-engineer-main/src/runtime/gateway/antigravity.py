from pathlib import Path
import traceback
import sys


def main():

    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    Path("artifacts/python_started.txt").write_text(
    "Python iniciou.",
    encoding="utf-8",
    )

    try:

        data = sys.stdin.read()

        (artifacts / "stdin.txt").write_text(
            data,
            encoding="utf-8",
        )

    except Exception:

        (artifacts / "gateway_error.txt").write_text(
            traceback.format_exc(),
            encoding="utf-8",
        )

    print("{}")


if __name__ == "__main__":
    main()