import os
import pytest
from src.commands.mv import mv_command


def test_no_args():
    with pytest.raises(ValueError, match="Ошибка в синтаксисе команды"):
        mv_command([])


def test_single_file(change_to_temp_dir):
    mv_command(["file.txt", "renamed.txt"])
    assert not os.path.exists("file.txt")
    assert os.path.exists("renamed.txt")
    with open("renamed.txt") as f:
        assert f.read() == "cheto"


def test_single_dir(change_to_temp_dir):
    mv_command(["folder", "renamed_folder"])
    assert not os.path.exists("folder")
    assert os.path.exists("renamed_folder")
    assert os.path.exists(os.path.join("renamed_folder", "another.txt"))


def test_single_to_existing_dir(change_to_temp_dir):
    os.mkdir("hm")
    mv_command(["file.txt", "hm"])
    assert not os.path.exists("file.txt")
    moved_file = os.path.join("hm", "file.txt")
    assert os.path.exists(moved_file)
    with open(moved_file) as f:
        assert f.read() == "cheto"


def test_error_not_exists(change_to_temp_dir):
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный файл"):
        mv_command(["nonexist.txt", "non.txt"])


def test_multiple_files_to_dir(change_to_temp_dir):
    with open("file2.txt", "w") as f:
        f.write("hehe")

    os.mkdir("hm")
    mv_command(["file.txt", "file2.txt", "hm"])

    assert not os.path.exists("file.txt")
    assert not os.path.exists("file2.txt")

    assert os.path.exists(os.path.join("hm", "file.txt"))
    assert os.path.exists(os.path.join("hm", "file2.txt"))

    with open(os.path.join("hm", "file2.txt")) as f:
        assert f.read() == "hehe"


def test_error_destination_not_exists(change_to_temp_dir):
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный файл"):
        mv_command(["file.txt", "file2.txt", "nonexist_dir"])
