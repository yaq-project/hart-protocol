from . import tools


def read_unique_identifier(address: bytes) -> bytes:
    return tools.pack_command(address, 0)


def read_primary_variable(address: bytes) -> bytes:
    return tools.pack_command(address, 1)


def read_unique_identifier_associated_with_tag(tag: bytes, *, address:int=0) -> bytes:
    return tools.pack_command(address, 11, tag)
