import pytest
from src.commands.cat import cat_command


def test_error_no_args():
    with pytest.raises(ValueError, match="Ошибка в синтаксисе команды"):
        cat_command([])


def test_error_file_not_exists():
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный файл"):
        cat_command(["nonexist.txt"])


def test_error_path_is_directory(change_to_temp_dir):
    with pytest.raises(IsADirectoryError, match="Отказано в доступе"):
        cat_command(["folder"])


def test_read_text(change_to_temp_dir):
    content = cat_command(["file.txt"])
    assert content == "cheto"


def test_error_not_text_file(change_to_temp_dir, monkeypatch):
    bin_file = "binary.bin"
    with open(bin_file, "wb") as f:
        f.write(b"\xFF\xFE")

    with pytest.raises(ValueError, match="не является текстовым файлом"):
        cat_command([bin_file])


def test_error_permission(change_to_temp_dir, monkeypatch):
    def fake_open(*args, **kwargs):
        raise PermissionError("Mocked permission denied")

    monkeypatch.setattr("builtins.open", fake_open)

    with pytest.raises(PermissionError, match="Нет доступа к файлу"):
        cat_command(["file.txt"])


def test_error_inability_to_read(change_to_temp_dir, monkeypatch):
    def fake_open(*args, **kwargs):
        raise OSError("Disk read error")

    monkeypatch.setattr("builtins.open", fake_open)

    with pytest.raises(Exception, match="Ошибка при чтении файла"):
        cat_command(["file.txt"])
