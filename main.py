import importlib
from time import perf_counter


year = 2015
day = 1
problem = 1


def main():
    module = importlib.import_module(f"{year}.{day}", package=".")
    function = getattr(module, f"problem_{problem}")
    function()


if __name__ == "__main__":
    start = perf_counter()
    main()
    print(f"Day {day}, problem {problem} completed in {perf_counter() - start:.3f}s")
