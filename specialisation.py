import argparse

import specialist


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("year")
    parser.add_argument("day")
    parser.add_argument("part")
    args = parser.parse_args()

    year = args.year
    day = args.day
    part = args.part

    specialist.main(("--targets", f"{year}/{day.zfill(2)}.py", "main.py", year, day, part))


if __name__ == "__main__":
    main()
