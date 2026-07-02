import json
import sys


def main():

    payload = json.load(sys.stdin)

    print(
        json.dumps(
            payload,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":

    main()