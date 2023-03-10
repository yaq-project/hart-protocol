# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2023.3.0]

### Changed
- in responses, device_status and response_code are now unpacked as two separate bytes
- data with bytecount of 2 has status only, and now returns immediately

## [2022.8.2]

### Fixed
- if the unpacker "ran ahead" of the serial buffer it would not succeed next time

## [2022.8.1]

### Fixed
- unpacker was broken in an async context

## [2022.8.0]

### Added
- initial release

[Unreleased]: https://github.com/yaq-project/hart-protocol/compare/v2023.3.0...main
[2023.3.0]: https://github.com/yaq-project/hart-protocol/compare/v2022.8.2...v2023.3.0
[2022.8.2]: https://github.com/yaq-project/hart-protocol/compare/v2022.8.1...v2022.8.2
[2022.8.1]: https://github.com/yaq-project/hart-protocol/compare/v2022.8.0...v2022.8.1
[2022.8.0]: https://gitlab.com/yaq/yaqd-picotech/tags/v2022.8.0
