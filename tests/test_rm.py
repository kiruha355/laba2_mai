import os
import pytest
from src.commands.rm import rm_command


def test_no_args():
    with pytest.raises(ValueError, match="Ошибка в синтаксисе команды"):
        rm_command([])


def test_file_not_exists():
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный файл"):
        rm_command(["nonexist.txt"])


def test_temp_file(change_to_temp_dir):
    with open("temp_file.txt", "w") as f:
        f.write("vse")
    assert os.path.exists("temp_file.txt")
    rm_command(["temp_file.txt"])
    assert not os.path.exists("temp_file.txt")


def test_directory_without_r(change_to_temp_dir):
    os.mkdir("empty_dir")
    with pytest.raises(ValueError, match="'empty_dir' является каталогом"):
        rm_command(["empty_dir"])


def test_directory_with_r(change_to_temp_dir, monkeypatch):
    os.mkdir("temp_dir")
    with open("temp_dir/another.txt", "w") as f:
        f.write("cheto")
    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)
    rm_command(["-r", "temp_dir"])
    assert not os.path.exists("temp_dir")


def test_delete_root_protected(change_to_temp_dir):
    root = os.path.abspath("/")
    with pytest.raises(ValueError, match="Запрещено удалять корневой"):
        rm_command([root])


def test_delete_parent_protected(change_to_temp_dir):
    with pytest.raises(ValueError, match="Запрещено удалять"):
        rm_command([".."])


def test_error_permission(change_to_temp_dir, monkeypatch):
    with open("protected.txt", "w") as f:
        f.write("protected")

    def mock_remove(path):
        raise PermissionError("Mocked permission error")

    monkeypatch.setattr("os.remove", mock_remove)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)
    with pytest.raises(PermissionError, match="Нет прав доступа"):
        rm_command(["protected.txt"])
