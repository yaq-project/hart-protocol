from . import tools


def read_unique_identifier(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=0)


def read_primary_variable(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=1)


def read_loop_current_and_percent(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=2)


def read_dynamic_variables_and_loop_current(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=3)


def write_polling_address(address: bytes, new_polling_address: int) -> bytes:
    assert 0 <= new_polling_address <= 15
    return tools.pack_command(address, command_id=6, data=new_polling_address.to_bytes(1, "big"))


def read_unique_identifier_associated_with_tag(tag: bytes, *, address: int = 0) -> bytes:
    return tools.pack_command(address, command_id=11, data=tag)


def read_message(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=12)


def read_tag_descriptor_date(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=13)


def read_primary_variable_information(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=14)


def read_output_information(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=15)


def read_final_assembly_number(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=16)


def write_message(address: bytes, message: str) -> bytes:
    message = message.ljust(32)
    return tools.pack_command(address, command_id=17, data=tools.pack_ascii(message))


def write_tag_descriptor_date(address: bytes, tag: str, descriptor: str, date: tuple):
    data = b""
    assert len(tag) <= 8
    data += tools.pack_ascii(tag.ljust(8))
    assert len(descriptor) <= 16
    data += tools.pack_ascii(descriptor.ljust(16))
    day, month, year = date
    data += day.to_bytes(1, "big")
    data += month.to_bytes(1, "big")
    data += year.to_bytes(1, "big")
    return tools.pack_command(address, command_id=18, data=data)


def write_final_assembly_number(address: bytes, number: int):
    data = number.to_bytes(3, "big")
    return tools.pack_command(address, command_id=19, data=data)
