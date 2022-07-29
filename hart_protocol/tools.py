import math
from typing import Union


def calculate_checksum(command: Union[int, bytes]) -> bytes:
    if type(command) == int:
        command = command.to_bytes(64, "big")  # type: ignore
    lrc = 0
    for byte in command:  # type: ignore
        lrc ^= byte
    out = lrc.to_bytes(1, "big")
    return out


def calculate_long_address(manufacturer_id: int, manufacturer_device_type: int, device_id: bytes):
    out = int.from_bytes(device_id, "big")
    out |= manufacturer_device_type << 24
    out |= manufacturer_id << 32
    return out.to_bytes(5, "big")


def pack_command(address, command_id, data=None):
    if type(address) == bytes:
        address = int.from_bytes(address, "big")
    if type(command_id) == int:
        command_id = command_id.to_bytes(1, "big")
    command = b"\xFF\xFF\xFF\xFF\xFF"  # preamble
    command += b"\x82"  # start charachter
    command += (549755813888 | address).to_bytes(5, "big")
    command += command_id
    if data is None:
        command += b"\x00"  # byte count
    else:
        command += len(data).to_bytes(1, "big")  # byte count
        command += data  # data
    command += calculate_checksum(command[5:])
    return command


def pack_ascii(string: Union[str, bytes]) -> bytes:
    if type(string) == str:
        chars = [c.encode() for c in string]  # type: ignore
    else:
        chars = [c for c in string]  # type: ignore
    out = 0
    for i, c in zip(range(8), [ord(c) & 0b0011_1111 for c in chars][::-1]):
        out |= c << (i * 6)
    return out.to_bytes(math.ceil((len(string) * 6) / 8), "big")
