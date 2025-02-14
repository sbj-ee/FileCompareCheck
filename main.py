import hashlib
import glob
from collections import Counter


def most_frequent(input_list):
    occurrence_count = Counter(input_list)
    return occurrence_count.most_common(1)[0][0]

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

    file_hash_list = []
    file_hash_dict = {}
    for test_file in test_files:
        file_hash = md5(test_file)
        print(f"{file_hash} : {test_file}")
        file_hash_list.append(file_hash)
        file_hash_dict[file_hash] = test_file

    file_hash_set = set(file_hash_list)
    print(f"There are {len(file_hash_set)} unique MD5 values")
    print(f"The most frequent hash is {most_frequent(file_hash_list)}")
    

if __name__ == "__main__":
    main()
