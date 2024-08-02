import numpy as np
from more_itertools import split_before


with open("./2018/resources/4.txt") as f:
    lines = f.read().splitlines()


def problem_1() -> None:
    num_nights = sum((1 for line in lines if "#" in line))
    sorted_lines = sorted(lines)
    guard_numbers: set[int] = set()
    date_and_id = np.empty((num_nights, 3), dtype=int)
    sleep_records = np.zeros((num_nights, 60), dtype=bool)
    for i, block_of_lines in enumerate(split_before(sorted_lines, lambda line: "#" in line)):
        guard_number = int(block_of_lines[0].split()[3][1:])
        guard_numbers.add(guard_number)
        month = int(block_of_lines[-1][6:8])
        day = int(block_of_lines[-1][9:11])
        date_and_id[i, :] = np.array([guard_number, month, day])
        for sleep_record, wake_record in zip(block_of_lines[1::2], block_of_lines[2::2]):
            start_minute = int(sleep_record[15:17])
            end_minute = int(wake_record[15:17])
            sleep_records[i, start_minute:end_minute] = True

    most_time_asleep_guard, most_time_asleep = 0, 0
    for guard_number in guard_numbers:
        (indices,) = np.where(date_and_id[:, 0] == guard_number)
        time_asleep = np.sum(sleep_records[indices, :])
        if time_asleep > most_time_asleep:
            most_time_asleep = time_asleep
            most_time_asleep_guard = guard_number
    (indices,) = np.where(date_and_id[:, 0] == most_time_asleep_guard)
    minute_most_asleep = np.argmax(np.sum(sleep_records[indices, :], axis=0))
    print(most_time_asleep_guard * minute_most_asleep)


def problem_2() -> None:
    num_nights = sum((1 for line in lines if "#" in line))
    sorted_lines = sorted(lines)
    guard_numbers: set[int] = set()
    date_and_id = np.empty((num_nights, 3), dtype=int)
    sleep_records = np.zeros((num_nights, 60), dtype=bool)
    for i, block_of_lines in enumerate(split_before(sorted_lines, lambda line: "#" in line)):
        guard_number = int(block_of_lines[0].split()[3][1:])
        guard_numbers.add(guard_number)
        month = int(block_of_lines[-1][6:8])
        day = int(block_of_lines[-1][9:11])
        date_and_id[i, :] = np.array([guard_number, month, day])
        for sleep_record, wake_record in zip(block_of_lines[1::2], block_of_lines[2::2]):
            start_minute = int(sleep_record[15:17])
            end_minute = int(wake_record[15:17])
            sleep_records[i, start_minute:end_minute] = True

    total_sleep_records = np.empty((len(guard_numbers), 60), dtype=int)
    unique_guard_numbers = np.array([x for x in guard_numbers])
    for i, guard_number in enumerate(unique_guard_numbers):
        (indices,) = np.where(date_and_id[:, 0] == guard_number)
        total_sleep_records[i, :] = np.sum(sleep_records[indices, :], axis=0)
    guard_index, minute = np.unravel_index(np.argmax(total_sleep_records), total_sleep_records.shape)
    print(unique_guard_numbers[guard_index] * minute)
