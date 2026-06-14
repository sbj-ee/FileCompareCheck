# FileCompareCheck

MD5-based file comparison utility for detecting identical and different files in a directory.

## Features

- Hash multiple files and group them by digest to see which are identical
- Report files that differ from the majority
- Choose the hash algorithm (`md5`, `sha256`, `sha1`, `blake2b`, ...)
- No external dependencies — standard library only
- Useful for comparing configuration files across systems

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
# No external dependencies required
```

## Usage

```bash
# Compare every *.txt file in the current directory (default)
python main.py

# Compare a specific set of files
python main.py path/to/*.conf

# Use a different hash algorithm
python main.py -a sha256 file1.txt file2.txt
```

## Example

Useful for checking if network configuration files from different routers should be identical:

```
$ python main.py
4221d002ceb5d3c9e9137e495ceaa647 : file1.txt
4221d002ceb5d3c9e9137e495ceaa647 : file2.txt
4221d002ceb5d3c9e9137e495ceaa647 : file3.txt
8556852b063d5ec80a717166b8e3e81f : file4.txt

There are 2 unique md5 values across 4 files
Files that differ from the majority:
  file4.txt
```

Files with matching hashes (file1, file2, file3) are identical. File4 has a different hash, indicating different content.

> **Note:** MD5 is fine for spotting accidental differences but is not collision-resistant. Use `-a sha256` if you need protection against deliberately crafted files.

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

## Requirements

- Python 3.x
