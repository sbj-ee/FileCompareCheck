# FileCompareCheck

MD5-based file comparison utility for detecting identical and different files in a directory.

## Features

- Calculate MD5 hashes for multiple files
- Identify which files are identical and which differ
- Useful for comparing configuration files across systems

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
# No external dependencies required
```

## Usage

```bash
python main.py
```

## Example

Useful for checking if network configuration files from different routers should be identical:

```
$ python main.py
4221d002ceb5d3c9e9137e495ceaa647 : file1.txt
4221d002ceb5d3c9e9137e495ceaa647 : file2.txt
4221d002ceb5d3c9e9137e495ceaa647 : file3.txt
8556852b063d5ec80a717166b8e3e81f : file4.txt
```

Files with matching hashes (file1, file2, file3) are identical. File4 has a different hash, indicating different content.

## Requirements

- Python 3.x
