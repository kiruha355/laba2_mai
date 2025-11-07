import os
import pytest
from src.commands.cp import cp_command


def test_no_args():
    with pytest.raises(ValueError, match="Невозможно скопировать файл поверх самого себя"):
        cp_command([])


def test_source_not_exists():
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный файл"):
        cp_command(["/nonexist", "/tmp/dest"])


def test_copy_file(change_to_temp_dir):
    source = "file.txt"
    dest = "file_copy.txt"
    cp_command([source, dest])
    assert os.path.exists(dest)
    with open(dest) as f:
        assert f.read() == "cheto"


def test_copy_dir_without_r(change_to_temp_dir):
    with pytest.raises(ValueError, match="Не удается найти указанный файл"):
        cp_command(["folder", "folder_copy"])


def test_copy_dir_with_r(change_to_temp_dir):
    cp_command(["-r", "folder", "folder_copy"])
    assert os.path.isdir("folder_copy")
    assert os.path.exists(os.path.join("folder_copy", "another.txt"))
    with open(os.path.join("folder_copy", "another.txt")) as f:
        assert f.read() == "postavte 90 ballov pls"


def test_error_permission(monkeypatch, change_to_temp_dir):
    def mock_copy2(*args, **kwargs):
        raise PermissionError("Mocked permission denied")

    monkeypatch.setattr("shutil.copy2", mock_copy2)

    with pytest.raises(PermissionError, match="Нет прав доступа для копирования"):
        cp_command(["file.txt", "protected_copy.txt"])


def test_error_inability_copy(monkeypatch, change_to_temp_dir):
    def mock_copy2(*args, **kwargs):
        raise OSError("Some I/O error")

    monkeypatch.setattr("shutil.copy2", mock_copy2)

    with pytest.raises(Exception, match="Невозможность копирования"):
        cp_command(["file.txt", "bad_copy.txt"])
