# Scotch Plains Rescue Squad - Crew Time Card Reader

## Purpose

Crew members tap their RFID cards/keychains at begin and end of crew, which will allow timesheet like processing and LOSAP input.

## Usage

TODO

## Repo Layout
- `src` Python source code
- `test` Tests, automated and manual
- `doc` Documentation
- `assets` Images, supporting documents

## Design

Two RFID card readers are attached to a computer.

A Python script monitors card reader outputs, detects reader activation, and extracts card facility and user codes.

The script enters card numbers into a google sheet document with the timestamp of reading.

Intended to work without a display, it gives user feedback through text-to-speech voice output.

##  Installation

### Python

Requires Python 3.10. Other versions might not work due to limitations in the text to speech module.

Requires workaround for incorrect file info for `en_US-lessac-medium.onnx.json` in `piper/voices.json` to avoid repeated download. Use patch:

```sh
patch $VIRTUAL_ENV/lib/python3.10/site-packages/piper/voices.json piper_120_voices.patch
```

### Windows 

Download `piper_windows_amd64.zip` from [piper-tts releases](https://github.com/rhasspy/piper/releases). Unzip into this folder, such that you can call `piper\piper.exe` from the commandline when being in the same folder as the json configuration files.

#### Startup Shortcut

Tested with automatic login of a dedicated non-admin account and link in the user's startup link folder.

### Linux

In order to make all tests work, a symbolic link is required for the external tts engine, like this:

```sh
mkdir piper
ln -s $(which piper) piper/
```

## Author

Written by info@eeproto.com, 2024, for the Scotch Plains Rescue Squad

## License

This work is available under the [Creative Commons Attribution-ShareAlike License 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) CC BY-NC-SA 4.0.
