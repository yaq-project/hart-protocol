# hart-protocol

[![PyPI](https://img.shields.io/pypi/v/hart-protocol)](https://pypi.org/project/hart-protocol)
[![Conda](https://img.shields.io/conda/vn/conda-forge/hart-protocol)](https://anaconda.org/conda-forge/hart-protocol)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![ver](https://img.shields.io/badge/calver-YYYY.M.MICRO-blue)](https://calver.org/)
[![log](https://img.shields.io/badge/change-log-informational)](https://github.com/yaq-project/hart-protocol/-/blob/main/CHANGELOG.md)

A sans I/O Python implementation of the [Highway Adressable Remote Transducer Protocol](https://en.wikipedia.org/wiki/Highway_Addressable_Remote_Transducer_Protocol).

## Introduction

This Python package contains tooling for encoding and decoding bytestrings for communication with HART peripherals.
HART has been implemented using a variety of transport layers---Bell 202, RS485, Ethernet, etc.
In persuit of simplicity and reusability, this package does not contain any interface capabilities.
Use something like [pySerial](https://pyserial.readthedocs.io) for transport.
Read the [sans I/O manifesto](https://sans-io.readthedocs.io/) for more motivation regarding this design pattern.

Briefly, HART is an open protocol for industrial automation supported by multiple device manufacturers.
HART has a concept of "address", so that many peripherals can share the same communication channel.
HART has limited support for multiple controllers, and generic handheld controllers exist.
HART peripherals respond to numbered commands, which can be thought of as primative [remote procedure calls](https://en.wikipedia.org/wiki/Remote_procedure_call).
The standard specifies a number of universal commands which should be supported by any peripheral, and there are also so-called "common" commands which many peripherals implement.
It's strongly recommended that you check the documentation of your own peripheral---implementations may be inconsistent.
In addition to universal and common commands, it's likely that your peripheral implements many device-specific commands.

This package aims to have complete and accurate support for all universal and common commands.
In addition, this package has tooling for packing and unpacking generic command data for device-specific commands.
This package is intentionally simple and narrowly scoped.
There is no documentation beyond this README.
Please open an issue or PR to the GitHub repository if you find any errors or missing functionality.

## Sending Commands

The following functions return bytestrings that can be fed to your transport layer.

Universal Commands
| command | function                                                    |
| ------- | ----------------------------------------------------------- |
| 0       | `read_unique_identifier(address)`                           |
| 1       | `read_primary_variable(address)`                            |
| 2       | `read_loop_current_and_percent(address)`                    |
| 3       | `read_dynamic_variables_and_loop_current(address)`          |
| 6       | `write_polling_address(address, new_short_address)`         |
| 11      | `read_unique_identifier_associated_with_tag(tag)`           |
| 12      | `read_message(address)`                                     |
| 13      | `read_tag_descriptor_date(address)`                         |
| 14      | `read_primary_variable_information(address)`                |
| 15      | `read_output_information(address)`                          |
| 16      | `read_final_assembly_number(address)`                       |
| 17      | `write_message(address, message)`                           |
| 18      | `write_tag_descriptor_date(address, tag, descriptor, date)` |
| 19      | `write_final_assembly_number(address, number)`              |

Common-Practice Commands
| command | function                                                 |
| ------- | -------------------------------------------------------- |
| 37      | `set_primary_variable_lower_range_value(address, value)` |
| 38      | `reset_configuration_changed_flag(address)`              |
| 42      | `perform_master_reset(address)`                          |
| 48      | `read_additional_transmitter_status(address)`            |
| 50      | `read_dynamic_variable_assignments(address)`             |
| 59      | `write_number_of_response_preambles(address, number)`    |
| 66      | `toggle_analog_output_mode(address)`                     |
| 67      | `trim_analog_output_zero(address)`                       |
| 68      | `trim_analog_output_span(address)`                       |
| 123     | `select_baud_rate(address, rate)`                        |

Arbitrary additional command bytestrings can also be generated as shown below.
This is a device-specific command for Brooks GF40 Mass Flow Controllers, which takes an IEE-754 floating point number as well as a unique code.

```python
import struct
import hart_protocol
code = 0
value = 32.1
data = struct.pack(">Bf", code, value)
command = hart_protocol.pack_command(address=123, command_id=236, data=data)
```

## Parsing Responses

All responses are parsed into named tuples.
Every single response will have the following keys.

Generic Response
| key             | value     |
| --------------- | --------- |
| `address`       | `<int>`   |
| `bytecount`     | `<int>`   |
| `command`       | `<int>`   |
| `command_name`  | `<str>`   |
| `data`          | `<bytes>` |
| `full_response` | `<bytes>` |
| `status`        | `<int>`   |

You can parse the raw `data` according to the particulars of your peripheral.
Certain standard responses are parsed further as shown below.

Response 0
| key                                           | value                      |
| --------------------------------------------- | -------------------------- |
| `command_name`                                | `"read_unique_identifier"` |
| `command`                                     | `0`                        |
| `device_id`                                   | `<bytes>`                  |
| `hardware_revision_level`                     | `<int>`                    |
| `manufacturer_device_type`                    | `<bytes>`                  |
| `manufacturer_id`                             | `<int>`                    |
| `number_response_preamble_charachters`        | `<int>`                    |
| `software_revision_level`                     | `<int>`                    |
| `transmitter_specific_command_revision_level` | `<int>`                    |
| `universal_command_revision_level             | `<int>`                    |

Response 1
| key                | value                     |
| ------------------ | ------------------------- |
| `command_name`     | `"read_primary_variable"` |
| `command`          | `1`                       |
| `primary_variable` | `<float>`                 |

Response 11
| key                                           | value                      |
| --------------------------------------------- | -------------------------- |
| `command_name`                                | `"read_unique_identifier"` |
| `command`                                     | `11`                       |
| `device_id`                                   | `<bytes>`                  |
| `hardware_revision_level`                     | `<int>`                    |
| `manufacturer_device_type`                    | `<bytes>`                  |
| `manufacturer_id`                             | `<int>`                    |
| `number_response_preamble_charachters`        | `<int>`                    |
| `software_revision_level`                     | `<int>`                    |
| `transmitter_specific_command_revision_level` | `<int>`                    |
| `universal_command_revision_level             | `<int>`                    |

## Integration Example

```python
>>> import hart_protocol
>>> import serial
>>>
>>> port = serial.Serial("/dev/ttyUSB0", 19200, timeout=0.1)
>>> port.parity = "O"
>>> port.stopbits = 1
>>> tag = hart_protocol.tools.pack_ascii("06C22300517"[-8:])
>>> port.write(hart_protocol.universal.read_unique_identifier_associated_with_tag(tag))
>>>
>>> unpacker = hart_protocol.Unpacker(port)
>>> for msg in unpacker:
...     print(msg)
...
>>>
```

## Maintainers

- [Blaise Thompson](https://github.com/untzag)
