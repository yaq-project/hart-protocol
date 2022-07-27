import struct




def parse(response: bytes) -> dict:
    out = dict()
    out["full_response"]: bytes = response
    if response[0] & 0x80:  # long address
        out["address"]: bytes = response[1:6]
        response = response[6:]
    else:  # short address
        out["address"]: bytes = response[1]
        response = response[2:]
    command, bytecount, status = struct.unpack_from(">BBL", response)
    out["status"] = status
    data = response[4:4+bytecount]
    out["command"]: int = command
    out["command_name"]: str = f"hart_command_{command}"
    out["bytecount"]: int = bytecount
    out["data"]: bytes = data
    if command in [0, 11]:
        out["command_name"] = "read_unique_identifier"
        out["manufacturer_id"]: bytes = data[1]
        out["manufacturer_device_type"]: bytes = data[2]
        out["number_response_preamble_characters"]: bytes = data[3]
        out["universal_command_revision_level"]: bytes = data[4]
        out["transmitter_specific_command_revision_level"]: bytes = data[5]
        out["software_revision_level"]: bytes = data[6]
        out["hardware_revision_level"]: bytes = data[7]
        out["device_id"]: bytes = data[9:12]
    if command in [1]:
        out["command_name"] = "read_primary_variable"
        out["primary_variable"] = struct.unpack_from(">f", data)
    return out
