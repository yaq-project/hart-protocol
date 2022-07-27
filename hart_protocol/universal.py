from . import tools


def read_unique_identifier(address: bytes) -> bytes:
    command = b"\xFF\xFF\xFF\xFF\xFF"  # preamble
    command += b"\x82"  # start charachter
    command += b"\x80\x00\x00\x00\x00"  # address of sender
    command += b"\x00"  # command ID (0)
    command += b"\x00"  # byte count
    command += tools.calculate_checksum(command[5:])
    return command


def read_primary_variable(address: bytes) -> bytes:
    command = b"\xFF\xFF\xFF\xFF\xFF"  # preamble
    command += b"\x82"  # start charachter
    command += b"\x80\x00\x00\x00\x00"  # address of sender
    command += b"\x01"  # command ID (1)
    command += b"\x00"  # byte count
    command += tools.calculate_checksum(command[5:])
    return command


def read_unique_identifier_associated_with_tag(tag: bytes) -> bytes:
    assert len(tag) == 6
    command = b"\xFF\xFF\xFF\xFF\xFF"  # preamble
    command += b"\x82"  # start charachter
    command += b"\x80\x00\x00\x00\x00"  # address of sender
    command += b"\x0B"  # command ID (11)
    command += b"\x06"  # byte count
    command += tag
    command += tools.calculate_checksum(command[5:])
    return command
