from collections import Counter


with open('./2016/resources/4.txt') as f:
    rooms = [line.strip() for line in f]


def problem_1():
    valid_sector_id_sum = 0

    for room in rooms:
        name, _, sector_id_and_checksum = room.rpartition("-")
        sector_id = int(sector_id_and_checksum[:sector_id_and_checksum.index("[")])
        checksum = sector_id_and_checksum[sector_id_and_checksum.index("[")+1:-1]

        frequencies = Counter(char for char in name if char != "-")
        sorted_frequencies = sorted(frequencies, key=lambda c: (frequencies[c], 25 - ord(c)), reverse=True)[:5]

        if "".join(sorted_frequencies) == checksum:
            valid_sector_id_sum += sector_id
    
    print(valid_sector_id_sum)


def problem_2():
    for room in rooms:
        name, _, sector_id_and_checksum = room.rpartition("-")
        sector_id = int(sector_id_and_checksum[:sector_id_and_checksum.index("[")])

        decrypted = "".join(" " if c == "-" else chr((ord(c) - 97 + sector_id) % 26 + 97) for c in name)
        
        if decrypted == "northpole object storage":
            print(sector_id)
            break
