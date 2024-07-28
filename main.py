import importlib
from time import perf_counter


year = 2018
day = 21
problem = 2


def main():
    start = perf_counter()
    module = importlib.import_module(f"{year}.{str(day).zfill(2)}", package=".")
    function = getattr(module, f"problem_{problem}")
    try:
        function()
    except KeyboardInterrupt:
        print(f"{year} day {day}, problem {problem} cancelled after {perf_counter() - start:.3f}s")
    else:
        print(f"{year} day {day}, problem {problem} completed in {perf_counter() - start:.3f}s")


if __name__ == "__main__":
    main()
