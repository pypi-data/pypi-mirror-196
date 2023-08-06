# CLIFX <!-- omit in toc -->

Cross-platform CLI for LIFX devices

![demo.gif](demo.gif)

## Table of Contents <!-- omit in toc -->
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive](#interactive)
  - [Examples](#examples)
  - [Options](#options)
- [Script Template](#script-template)
  - [Windows](#windows)
  - [Linux/Mac](#linuxmac)
- [Development](#development)
  - [Installation](#installation-1)
  - [Usage](#usage-1)
  - [Build](#build)
- [Contributing](#contributing)
- [Links](#links)

## Installation

```bash
pip install clifx
```

## Usage

### Interactive

```bash
clifx  # interactive prompt - specify device and new hue, saturation, brightness and colour temp
```

### Examples

```bash
# set the device labelled 'Strip' to...
clifx -l Strip -h 50 -s 50 -v 50 -k 6500 # soft cyan with a daylight colour temp
clifx -l Strip -h 0 -s 100 -v 100 -k 6500 # pure red at 100% brightness
```

### Options
```bash
clifx --help  # display help
```

## Script Template

### Windows

_Contents of `<your-preset>.ps1`_

```powershell
# TODO
```

### Linux/Mac

_Contents of `<your-preset>.sh`:_

```sh
#!/bin/bash
clifx -l <device-label> -h <hue> -s <saturation> -v <value> -k <kelvin>
```

## Development

### Installation

```bash
git clone https://gitlab.com/DrTexx/CLIFX/
cd CLIFX
poetry install
```

### Usage

Identical to typical usage except commands must be prefixed by `poetry run`.

For example, instead of writing the following:

```bash
clifx
```

You would write this:

```bash
poetry run clifx
```

### Build

```bash
./development-scripts/build.sh
```

## Contributing

[Issues](https://gitlab.com/DrTexx/CLIFX/-/issues) and [pull requests](https://gitlab.com/DrTexx/CLIFX/-/merge_requests/new) welcome!

## Links

<!-- TODO: add Website link -->
- Documentation: https://gitlab.com/DrTexx/CLIFX#clifx
- PyPI Releases: https://pypi.org/project/clifx
- Source Code: https://gitlab.com/DrTexx/CLIFX/
- Issue Tracker: https://gitlab.com/DrTexx/CLIFX/-/issues
- Twitter: [@DrTexx](https://twitter.com/DrTexx)
- Email: [denver.opensource@tutanota.com](mailto:denver.opensource@tutanota.com)
