from . import tools


def set_primary_variable_lower_range_value(address: bytes, value) -> bytes:
    return tools.pack_command(address, command_id=37)


def reset_configuration_changed_flag(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=38)


def perform_master_reset(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=42)


def read_additional_transmitter_status(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=48)


def read_dynamic_variable_assignments(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=50)


def write_number_of_response_preambles(address: bytes, number: int) -> bytes:
    data = number.to_bytes(1, "big")  # check for bytes in manual
    return tools.pack_command(address, command_id=59, data=data)


def toggle_analog_output_mode(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=66)


def trim_analog_output_zero(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=67)


def trim_analog_output_span(address: bytes) -> bytes:
    return tools.pack_command(address, command_id=68)


def select_baud_rate(address: bytes, rate: int) -> bytes:
    data = rate.to_bytes(1, "big")  # check bytes in manual
    return tools.pack_command(address, command_id=123, data=data)
