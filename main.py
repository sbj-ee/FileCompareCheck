import argparse
import glob
import hashlib
from collections import defaultdict


def file_hash(filename, algorithm="md5"):
    """Compute the hash digest for a file, reading it in chunks."""
    hasher = hashlib.new(algorithm)
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def group_by_hash(filenames, algorithm="md5"):
    """Return a dict mapping each hash digest to the list of files with it."""
    groups = defaultdict(list)
    for filename in filenames:
        groups[file_hash(filename, algorithm)].append(filename)
    return groups


def main():
    parser = argparse.ArgumentParser(
        description="Compare files by hash to find which are identical and which differ."
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=None,
        help="Files to compare (default: *.txt in the current directory).",
    )
    # Exclude SHAKE algorithms: their hexdigest() requires an explicit length.
    algorithms = sorted(a for a in hashlib.algorithms_guaranteed if not a.startswith("shake"))
    parser.add_argument(
        "-a",
        "--algorithm",
        default="md5",
        choices=algorithms,
        help="Hash algorithm to use (default: md5).",
    )
    args = parser.parse_args()

    files = sorted(args.files) if args.files else sorted(glob.glob("*.txt"))
    if not files:
        parser.error("No files to compare.")

    try:
        groups = group_by_hash(files, args.algorithm)
    except OSError as e:
        parser.error(f"Could not read {e.filename}: {e.strerror}")

    for digest in sorted(groups, key=lambda d: (-len(groups[d]), groups[d][0])):
        for filename in sorted(groups[digest]):
            print(f"{digest} : {filename}")

    plural = "value" if len(groups) == 1 else "values"
    print(f"\nThere are {len(groups)} unique {args.algorithm} {plural} across {len(files)} files")

    # The largest group is treated as the "expected" content; everything else differs.
    largest = max(groups, key=lambda d: len(groups[d]))
    outliers = [f for d, fs in groups.items() if d != largest for f in fs]
    if outliers:
        print("Files that differ from the majority:")
        for filename in sorted(outliers):
            print(f"  {filename}")
    else:
        print("All files are identical.")


if __name__ == "__main__":
    main()
