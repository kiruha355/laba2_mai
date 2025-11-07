import os
import pytest
from src.commands.cd import cd_command


def test_no_args(initial_cwd):
    result = cd_command([])
    assert result == os.path.expanduser("~")


def test_tilde(initial_cwd):
    result = cd_command(["~"])
    assert result == os.path.expanduser("~")


def test_current(initial_cwd):
    original = os.getcwd()
    result = cd_command(["."])
    assert result == original


def test_parent(change_to_temp_dir):
    original = os.getcwd()
    parent = os.path.dirname(original)
    result = cd_command([".."])
    assert result == parent


def test_absolute_path(change_to_temp_dir, temp_dir):
    subdir = os.path.join(temp_dir, "folder")
    result = cd_command([subdir])
    assert result == subdir


def test_relative_path(change_to_temp_dir):
    os.mkdir("test")
    result = cd_command(["test"])
    expected = os.path.join(change_to_temp_dir, "test")
    assert result == expected


def test_nonexistent_path(change_to_temp_dir):
    with pytest.raises(FileNotFoundError, match="Системе не удается найти указанный путь"):
        cd_command(["nonexist_folder"])
