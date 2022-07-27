import math


def calculate_checksum(command: bytes) -> bytes:
    lrc = 0
    for byte in command:
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
    print(command)
    return command


def pack_ascii(string: str) -> bytes:
    chars = [c.encode() for c in string]
    chars = [ord(c) & 0b0011_1111 for c in chars]
    out = 0
    for i, c in zip(range(8), chars[::-1]):
        out |= c << (i * 6)
    out = out.to_bytes(math.ceil((len(string) * 6) / 8), "big")
    return out
