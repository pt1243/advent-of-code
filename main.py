import argparse
import importlib
from time import perf_counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int)
    args = parser.parse_args()

    year = args.year
    day = args.day
    part = args.part

    start = perf_counter()
    module = importlib.import_module(f"{year}.{str(day).zfill(2)}", package=".")
    function = getattr(module, f"part_{part}")
    try:
        function()
    except KeyboardInterrupt:
        print(f"{year} day {day}, part {part} cancelled after {perf_counter() - start:.3f}s")
    else:
        print(f"{year} day {day}, part {part} completed in {perf_counter() - start:.3f}s")


if __name__ == "__main__":
    main()
