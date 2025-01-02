# Scotch Plains Rescue Squad - Crew Time Card Reader

## Purpose

Crew members tap their RFID cards/keychains at begin and end of crew, which will allow timesheet like processing and LOSAP input.

## Usage

TODO

## Design

Two RFID card readers are attached to a computer.

A Python script monitors card reader outputs, detects reader activation, and extracts card facility and user codes.

The script enters card numbers into a google sheet document with the timestamp of reading.

## Windows Installation

### Python

Tested with 3.13.

### Startup Shortcut

TODO

### Autostart

Tested with automatic login of a dedicated non-admin account and link in the user's startup link folder.

## Author

Written by info@eeproto.com, 2024, for the Scotch Plains Rescue Squad

## License

This work is available under the [Creative Commons Attribution-ShareAlike License 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) CC BY-NC-SA 4.0.
