import importlib
from time import perf_counter


year = 2016
day = 6
problem = 2


def main():
    module = importlib.import_module(f"{year}.{day}", package=".")
    function = getattr(module, f"problem_{problem}")
    start = perf_counter()
    function()
    print(f"{year} day {day}, problem {problem} completed in {perf_counter() - start:.3f}s")


if __name__ == "__main__":
    main()
