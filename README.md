# hart-protocol

[![PyPI](https://img.shields.io/pypi/v/hart-protocol)](https://pypi.org/project/hart-protocol)
[![Conda](https://img.shields.io/conda/vn/conda-forge/hart-protocol)](https://anaconda.org/conda-forge/hart-protocol)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![ver](https://img.shields.io/badge/calver-YYYY.M.MICRO-blue)](https://calver.org/)
[![log](https://img.shields.io/badge/change-log-informational)](https://github.com/yaq-project/hart-protocol/-/blob/main/CHANGELOG.md)

A sans-io Python implementation of the [Highway Adressable Remote Transducer Protocol](https://en.wikipedia.org/wiki/Highway_Addressable_Remote_Transducer_Protocol).

Universal Commands
| command | function                          |
| ------- | --------------------------------- |
| 0       | `read_unique_identifier(address)` |
| 1       | `read_primary_variable(address)`  |
| 2       | `read_loop_current_and_percent(address)` |
| 3       | `read_dynamic_variables_and_loop_current(address)` |
| 4       |
| 5       |
| 6       |
| 11      |
| 12      |
| 13      |
| 14      |
| 15      |
| 16      |
| 17      |
| 18      |
| 19      |

Common-Practice Commands
| command | function                          |
| ------- | --------------------------------- |
| 33      |
| 38      |
| 40      |
| 42      |
| 44      |
| 45      |
| 46      |
| 48      |
| 50      |
| 51      |
| 53      |
| 54      |
| 59      |

Maintainers:

- [Blaise Thompson](https://github.com/untzag)
