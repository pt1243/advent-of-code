from dataclasses import dataclass
from math import ceil

with open("./2021/resources/16.txt") as f:
    packet_hex = f.read().strip()


@dataclass
class Packet:
    version: int
    type_id: int
    value: int


@dataclass
class OperatorPacket(Packet):
    subpackets: list[Packet]


def parse_packet(bits: str, index: int = 0) -> tuple[Packet, int]:
    version = int(bits[index : index + 3], 2)
    type_id = int(bits[index + 3 : index + 6], 2)
    index += 6
    if type_id == 4:
        value_string = ""
        while True:
            prefix = bits[index]
            value_string += bits[index + 1 : index + 5]
            index += 5
            if prefix == "0":
                break
        return Packet(version, type_id, int(value_string, 2)), index
    else:
        length_type_id = int(bits[index])
        index += 1
        subpackets: list[Packet] = []
        if length_type_id == 0:
            length_of_sub_packets = int(bits[index : index + 15], 2)
            index += 15
            end_index = index + length_of_sub_packets
            while index < end_index:
                subpacket, new_index = parse_packet(bits, index)
                subpackets.append(subpacket)
                index = new_index
        elif length_type_id == 1:
            num_subpackets = int(bits[index : index + 11], 2)
            index += 11
            for _ in range(num_subpackets):
                subpacket, new_index = parse_packet(bits, index)
                subpackets.append(subpacket)
                index = new_index
        else:
            raise ValueError(f"invalid length type ID {length_type_id}")
        if type_id == 0:
            value = sum(p.value for p in subpackets)
        elif type_id == 1:
            value = 1
            for p in subpackets:
                value *= p.value
        elif type_id == 2:
            value = min(p.value for p in subpackets)
        elif type_id == 3:
            value = max(p.value for p in subpackets)
        elif type_id == 5:
            if len(subpackets) != 2:
                raise ValueError("greater than packets must have exactly two subpackets")
            value = 1 if subpackets[0].value > subpackets[1].value else 0
        elif type_id == 6:
            if len(subpackets) != 2:
                raise ValueError("less than packets must have exactly two subpackets")
            value = 1 if subpackets[0].value < subpackets[1].value else 0
        elif type_id == 7:
            if len(subpackets) != 2:
                raise ValueError("equal to packets must have exactly two subpackets")
            value = 1 if subpackets[0].value == subpackets[1].value else 0
        else:
            raise ValueError(f"invalid type ID {type_id}")
        return OperatorPacket(version, type_id, value, subpackets), index


def problem_1() -> None:
    packet_bits = bin(int(packet_hex, 16))[2:]
    packet_bits = packet_bits.zfill(ceil(len(packet_bits) / 4) * 4)
    root_packet, _ = parse_packet(packet_bits)
    if not isinstance(root_packet, OperatorPacket):
        raise ValueError("root packet does not contain any subpackets")

    def sum_of_version_numbers(packet: Packet) -> int:
        if isinstance(packet, OperatorPacket):
            return packet.version + sum(sum_of_version_numbers(p) for p in packet.subpackets)
        return packet.version

    print(sum_of_version_numbers(root_packet))


def problem_2() -> None:
    packet_bits = bin(int(packet_hex, 16))[2:]
    packet_bits = packet_bits.zfill(ceil(len(packet_bits) / 4) * 4)
    root_packet, _ = parse_packet(packet_bits)

    print(root_packet.value)
