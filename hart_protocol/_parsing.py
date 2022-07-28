import struct
from typing import MutableMapping, Union


def parse(response: bytes) -> MutableMapping[str, Union[int, bytes, str, float]]:
    out: MutableMapping[str, Union[int, bytes, str, float]] = dict()
    out["full_response"] = response
    if response[0] & 0x80:  # long address
        out["address"] = int.from_bytes(response[1:6], "big")
        response = response[6:]
    else:  # short address
        out["address"] = response[1]
        response = response[2:]
    command, bytecount, status = struct.unpack_from(">BBL", response)
    out["status"] = status
    data = response[4 : 4 + bytecount]
    out["command"] = command
    out["command_name"] = f"hart_command_{command}"
    out["bytecount"] = bytecount
    out["data"] = data
    if command in [0, 11]:
        out["command_name"] = "read_unique_identifier"
        out["manufacturer_id"] = data[1]
        out["manufacturer_device_type"] = data[2]
        out["number_response_preamble_characters"] = data[3]
        out["universal_command_revision_level"] = data[4]
        out["transmitter_specific_command_revision_level"] = data[5]
        out["software_revision_level"] = data[6]
        out["hardware_revision_level"] = data[7]
        out["device_id"] = data[9:12]
    if command in [1]:
        out["command_name"] = "read_primary_variable"
        out["primary_variable"] = struct.unpack_from(">f", data)[0]
    return out
