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

    # universal commands
    if command in [0, 11]:
        out["command_name"] = "read_unique_identifier"
        out["manufacturer_id"] = data[1]
        out["manufacturer_device_type"] = data[2]
        out["number_response_preamble_characters"] = data[3]
        out["universal_command_revision_level"] = data[4]
        out["transmitter_specific_command_revision_level"] = data[5]
        out["software_revision_level"] = data[6]
        out["hardware_revision_level"] = data[7]
        out["device_id"] = int.from_bytes(data[9:12], "big")
    elif command in [1]:
        out["command_name"] = "read_primary_variable"
        units, variable = struct.unpack_from(">Bf", data)
        out["primary_variable_units"] = units
        out["primary_variable"] = variable
    elif command in [2]:
        out["command_name"] = "read_loop_current_and_percent"
        analog_signal, primary_variable = struct.unpack_from(">ff", data)
        out["analog_signal"] = analog_signal
        out["primary_variable"] = primary_variable
    elif command in [3]:
        out["command_name"] = "read_dynamic_variables_and_loop_current"
        (
            analog_signal,
            primary_variable_units,
            primary_variable,
            secondary_variable_units,
            secondary_variable,
        ) = struct.unpack_from(">fBfBf", data)
        out["analog_signal"] = analog_signal
        out["primary_variable_units"] = primary_variable_units
        out["primary_variable"] = primary_variable
        out["secondary_variable_units"] = secondary_variable_units
        out["secondary_variable"] = secondary_variable
    elif command in [6]:
        out["command_name"] = "write_polling_address"
        polling_address = struct.unpack_from(">B", data)[0]
        out["polling_address"] = polling_address
    elif command in [12]:
        out["command_name"] = "read_message"
        out["message"] = data[0:23]
    elif command in [13]:
        out["command_name"] = "read_tag_descriptor_date"
        out["device_tag_name"] = data[0:5]
        out["device_descriptor"] = data[6:17]
        out["date"] = data[18:20]
    elif command in [14]:
        out["command_name"] = "read_primary_variable_information"
        out["serial_no"] = data[0:2]
        sensor_limits_code, upper_limit, lower_limit, min_span = struct.unpack_from(
            ">xxxBfff", data
        )
        out["sensor_limits_code"] = sensor_limits_code
        out["upper_limit"] = upper_limit
        out["lower_limit"] = lower_limit
        out["min_span"] = min_span
    elif command in [15]:
        out["command_name"] = "read_output_information"
        (
            alarm_code,
            transfer_fn_code,
            primary_variable_range_code,
            upper_range_value,
            lower_range_value,
            damping_value,
            write_protect,
            private_label,
        ) = struct.unpack_from(">BBBfffBB", data)
        out["alarm_code"] = alarm_code
        out["transfer_fn_code"] = transfer_fn_code
        out["primary_variable_range_code"] = primary_variable_range_code
        out["upper_range_value"] = upper_range_value
        out["lower_range_value"] = lower_range_value
        out["damping_value"] = damping_value
        out["write_protect"] = write_protect
        out["private_label"] = private_label
    elif command in [16]:
        out["command_name"] = "read_final_assembly_number"
        out["final_assembly_no"] = int.from_bytes(data[0:2], "big")
    elif command in [17]:
        out["command_name"] = "write_message"
        out["message"] = data[0:23]
    elif command in [18]:
        out["command_name"] = "write_tag_descriptor_date"
        out["device_tag_name"] = data[0:5]
        out["device_descriptor"] = data[6:17]
        out["date"] = data[18:20]
    elif command in [19]:
        out["command_name"] = "write_final_assembly_number"
        out["final_assembly_no"] = int.from_bytes(data[0:2], "big")

    # COMMON COMMANDS

    # elif command in [37]:
    #     out["command_name"] = "set_primary_variable_lower_range_value"
    #     out[""] =
    # request data bytes = NONE, response data bytes = NONE

    # elif command in [38]:
    #     out["command_name"] = "reset_configuration_changed_flag"
    #     out[""] =
    # request data bytes = NONE, response data bytes = NONE

    # elif command in [42]:
    #     out["command_name"] = "perform_master_reset"
    #     out[""] =
    # request data bytes = NONE, response data bytes = NONE

    # elif command in [48]:
    #     out["command_name"] = "read_additional_transmitter_status"
    #     out[""] =
    # request data bytes = NONE, response data bytes = NONE

    elif command in [50]:
        out["command_name"] = "read_dynamic_variable_assignments"
        (
            primary_transmitter_variable,
            secondary_transmitter_variable,
            tertiary_transmitter_variable,
            quaternary_transmitter_variable,
        ) = struct.unpack_from(">BBBB", data)
        out["primary_transmitter_variable"] = primary_transmitter_variable
        out["secondary_transmitter_variable"] = secondary_transmitter_variable
        out["tertiary_transmitter_variable"] = tertiary_transmitter_variable  # NOT USED
        out["quaternary_transmitter_variable"] = quaternary_transmitter_variable  # NOT USED
    elif command in [59]:
        out["command_name"] = "write_number_of_response_preambles"
        n_response_preambles = struct.unpack_from(">B", data)[0]
        out["n_response_preambles"] = n_response_preambles
    elif command in [66]:
        out["command_name"] = "toggle_analog_output_mode"
        (
            analog_output_selection,
            analog_output_units_code,
            fixed_analog_output,
        ) = struct.unpack_from(">BBf", data)
        out["analog_output_selection"] = analog_output_selection
        out["analog_output_units_code"] = analog_output_units_code
        out["fixed_analog_output"] = fixed_analog_output
    elif command in [67]:
        out["command_name"] = "trim_analog_output_zero"
        analog_output_code, analog_output_units_code, measured_analog_output = struct.unpack_from(
            ">BBf", data
        )
        out["analog_output_code"] = analog_output_code
        out["analog_output_units_code"] = analog_output_units_code
        out["measured_analog_output"] = measured_analog_output
    elif command in [68]:
        out["command_name"] = "trim_analog_output_span"
        analog_output_code, analog_output_units_code, measured_analog_output = struct.unpack_from(
            ">BBf", data
        )
        out["analog_output_code"] = analog_output_code
        out["analog_output_units_code"] = analog_output_units_code
        out["measured_analog_output"] = measured_analog_output
    elif command in [123]:
        out["command_name"] = "select_baud_rate"
        out["baud_rate"] = int.from_bytes(data, "big")

    return out
