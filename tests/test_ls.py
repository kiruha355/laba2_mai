import pytest
import os
from src.commands.ls import ls_command, find_directory


def test_ls(change_to_temp_dir):
    result = ls_command([])
    assert "file.txt" in result
    assert "folder" in result
    assert isinstance(result, str)


def test_with_l(change_to_temp_dir):
    result = ls_command(["-l"])
    assert isinstance(result, str)
    assert "file.txt" in result
    assert "folder/" in result
    assert "-rw" in result


def test_explicit_path(temp_dir):
    result = ls_command([temp_dir])
    assert "file.txt" in result
    assert "folder" in result


def test_with_l_and_path(temp_dir):
    result = ls_command(["-l", temp_dir])
    assert isinstance(result, str)
    assert "folder/" in result


def test_nonexist_path():
    with pytest.raises(FileNotFoundError, match="Путь '/nonexist/path' не существует."):
        ls_command(["/nonexist/path"])


def test_error_is_file(temp_dir):
    file_path = os.path.join(temp_dir, "file.txt")
    with pytest.raises(NotADirectoryError) as exc_info:
        ls_command([file_path])
    assert str(exc_info.value) == f"'{file_path}' не является каталогом."


def test_find_directory_exists(change_to_temp_dir):
    result = find_directory("folder")
    expected = os.path.join(change_to_temp_dir, "folder")
    assert result == expected
