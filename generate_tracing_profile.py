"""Extremely hacky script to profile a solution and display the formatted results. Requires dot and yelp-gprof2dot to be
installed. Note that timing information should be taken from the outputs of main.py, as the tracing here will slow down
things considerably. Based on https://www.youtube.com/watch?v=ey_P64E34g0."""

import argparse
import cProfile
import importlib
import os
import tempfile
import time
import webbrowser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int)
    args = parser.parse_args()

    year = args.year
    day = args.day
    part = args.part

    module = importlib.import_module(f"{year}.{str(day).zfill(2)}", package=".")
    function = getattr(module, f"part_{part}")
    pr = cProfile.Profile()
    pr.runcall(function)
    with tempfile.TemporaryDirectory() as temp_dir:
        pr.dump_stats(f"{temp_dir}/log.pstats")
        os.system(f"gprof2dot {temp_dir}/log.pstats -n 0 -e 0 > {temp_dir}/graph")
        os.system(f"dot -Tsvg {temp_dir}/graph > {temp_dir}/img.svg")
        # very hacky: webbrowser.open does not block until the file has been opened, so sleep to prevent the temp dir
        # from being cleaned up
        webbrowser.open(f"{temp_dir}/img.svg")
        time.sleep(1)


if __name__ == "__main__":
    main()
