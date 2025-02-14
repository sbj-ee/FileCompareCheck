import hashlib
import glob


def md5(filename):
    """Compute the md5 for a file."""
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    test_files = glob.glob('*.txt')
    test_files.sort()

    for test_file in test_files:
        print(f"{md5(test_file)} : {test_file}")


if __name__ == "__main__":
    main()