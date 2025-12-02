import argparse

import specialist


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("year")
    parser.add_argument("day")
    parser.add_argument("problem")
    args = parser.parse_args()

    year = args.year
    day = args.day
    problem = args.problem

    specialist.main(("--targets", f"{year}/{day.zfill(2)}.py", "main.py", year, day, problem))


if __name__ == "__main__":
    main()
