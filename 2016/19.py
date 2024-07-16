from math import floor, log2, log


with open("./2016/resources/19.txt") as f:
    num_elves = int(f.read().strip())


def problem_1() -> None:
    # https://www.youtube.com/watch?v=uCsD3ZGzMgE
    max_pow_2 = floor(log2(num_elves))
    difference = num_elves - 2**max_pow_2
    print(2 * difference + 1)


def problem_2() -> None:
    max_pow_3 = 3 ** floor(log(num_elves, 3))
    if max_pow_3 == num_elves:
        ans = num_elves
    else:
        threshold = 2 * max_pow_3
        ans = num_elves - max_pow_3
        if num_elves > threshold:
            ans += num_elves - 2 * max_pow_3
    print(ans)
