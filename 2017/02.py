with open("./2017/resources/2.txt") as f:
    lines = f.read().splitlines()


def part_1() -> None:
    total_checksum = 0
    for line in lines:
        nums = [int(n) for n in line.split()]
        total_checksum += max(nums) - min(nums)
    print(total_checksum)


def part_2() -> None:
    total = 0
    for line in lines:
        nums = [int(n) for n in line.split()]
        found = False
        for i, num_1 in enumerate(nums):
            for num_2 in nums[i + 1 :]:
                if num_1 % num_2 == 0:
                    total += num_1 // num_2
                    found = True
                    break
                if num_2 % num_1 == 0:
                    total += num_2 // num_1
                    found = True
                    break
            if found:
                break
    print(total)
