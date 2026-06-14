import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

import main

REPO_ROOT = Path(__file__).resolve().parent.parent


def write(tmp_path, name, content):
    path = tmp_path / name
    path.write_bytes(content if isinstance(content, bytes) else content.encode())
    return path


# --- file_hash -------------------------------------------------------------


def test_file_hash_matches_hashlib(tmp_path):
    data = b"this is a test file\n"
    path = write(tmp_path, "a.txt", data)
    assert main.file_hash(str(path)) == hashlib.md5(data).hexdigest()


def test_file_hash_respects_algorithm(tmp_path):
    data = b"hello world"
    path = write(tmp_path, "a.txt", data)
    assert main.file_hash(str(path), "sha256") == hashlib.sha256(data).hexdigest()


def test_file_hash_handles_content_larger_than_chunk(tmp_path):
    # Larger than the 4096-byte read chunk to exercise the chunked loop.
    data = b"x" * 10000
    path = write(tmp_path, "big.txt", data)
    assert main.file_hash(str(path)) == hashlib.md5(data).hexdigest()


def test_file_hash_missing_file_raises(tmp_path):
    with pytest.raises(OSError):
        main.file_hash(str(tmp_path / "does-not-exist.txt"))


# --- group_by_hash ---------------------------------------------------------


def test_group_by_hash_groups_identical_files(tmp_path):
    a = write(tmp_path, "a.txt", "same")
    b = write(tmp_path, "b.txt", "same")
    c = write(tmp_path, "c.txt", "different")

    groups = main.group_by_hash([str(a), str(b), str(c)])

    assert len(groups) == 2
    sizes = sorted(len(v) for v in groups.values())
    assert sizes == [1, 2]


def test_group_by_hash_all_unique(tmp_path):
    files = [str(write(tmp_path, f"f{i}.txt", f"content-{i}")) for i in range(3)]
    groups = main.group_by_hash(files)
    assert len(groups) == 3


def test_group_by_hash_empty():
    assert main.group_by_hash([]) == {}


# --- CLI (main) ------------------------------------------------------------


def run_cli(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "main.py"), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def test_cli_reports_outliers(tmp_path):
    write(tmp_path, "a.txt", "same")
    write(tmp_path, "b.txt", "same")
    write(tmp_path, "c.txt", "odd")

    result = run_cli("a.txt", "b.txt", "c.txt", cwd=tmp_path)

    assert result.returncode == 0
    assert "There are 2 unique md5 values across 3 files" in result.stdout
    assert "Files that differ from the majority:" in result.stdout
    assert "c.txt" in result.stdout


def test_cli_all_identical(tmp_path):
    write(tmp_path, "a.txt", "same")
    write(tmp_path, "b.txt", "same")

    result = run_cli("a.txt", "b.txt", cwd=tmp_path)

    assert result.returncode == 0
    assert "1 unique md5 value across 2 files" in result.stdout
    assert "All files are identical." in result.stdout


def test_cli_defaults_to_txt_glob(tmp_path):
    write(tmp_path, "a.txt", "same")
    write(tmp_path, "ignored.log", "same")

    result = run_cli(cwd=tmp_path)

    assert result.returncode == 0
    assert "a.txt" in result.stdout
    assert "ignored.log" not in result.stdout


def test_cli_algorithm_choice(tmp_path):
    data = "hello"
    write(tmp_path, "a.txt", data)

    result = run_cli("-a", "sha256", "a.txt", cwd=tmp_path)

    assert result.returncode == 0
    assert hashlib.sha256(data.encode()).hexdigest() in result.stdout


def test_cli_missing_file_errors_cleanly(tmp_path):
    result = run_cli("nope.txt", cwd=tmp_path)

    assert result.returncode == 2
    assert "Could not read" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_no_files_errors(tmp_path):
    result = run_cli(cwd=tmp_path)  # empty dir, no *.txt

    assert result.returncode == 2
    assert "No files to compare." in result.stderr
