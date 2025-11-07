import os
import pytest
from src.commands.zip_and_tar import zip_command, unzip_command, tar_command, untar_command


def test_error_zip_command_no_args():
    with pytest.raises(ValueError, match="Не указано имя архива"):
        zip_command([])


def test_error_zip_command_invalid_end():
    with pytest.raises(ValueError, match="Не является ZIP файлом"):
        zip_command(["some_folder", "archive.txt"])


def test_error_zip_folder_not_exists(change_to_temp_dir):
    with pytest.raises(FileNotFoundError, match="Папка не найдена"):
        zip_command(["nonexist", "test.zip"])


def test_error_zip_source_is_file(change_to_temp_dir):
    with open("file.txt", "w") as f:
        f.write("cheto")
    with pytest.raises(ValueError, match="Не является папкой"):
        zip_command(["file.txt", "test.zip"])


def test_zip_command_create_archive(change_to_temp_dir):
    os.mkdir("project")
    with open("project/main.py", "w") as f:
        f.write("z")
    os.mkdir("project/data")
    with open("project/data/config.txt", "w") as f:
        f.write("z")
    zip_command(["project", "project.zip"])

    assert os.path.exists("project.zip")
    import zipfile
    with zipfile.ZipFile("project.zip", "r") as zf:
        file_list = zf.namelist()

        assert "main.py" in file_list
        assert "data/config.txt" in file_list


def test_unzip_command_extracts_archive(change_to_temp_dir):
    import zipfile

    with zipfile.ZipFile("test.zip", "w") as zf:
        zf.writestr("main.py", "z")
        zf.writestr("data/config.txt", "z")
    unzip_command(["test.zip"])

    assert os.path.exists("main.py")
    assert os.path.exists("data/config.txt")


def test_error_unzip_archive_not_exists():
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный ZIP"):
        unzip_command(["fake.zip"])


def test_error_unzip_invalid_file(change_to_temp_dir):
    with open("fake.zip", "w") as f:
        f.write("zzzzzzzz")
    with pytest.raises(ValueError, match="Не является ZIP файлом"):
        unzip_command(["fake.zip"])


def test_error_tar_command_no_args():
    with pytest.raises(ValueError, match="Не указана папка"):
        tar_command([])
    with pytest.raises(ValueError, match="Не указана папка"):
        tar_command(["only_folder"])


def test_error_tar_command_invalid_extension():
    with pytest.raises(ValueError, match="Не является TAR.GZ файлом"):
        tar_command(["folder", "archive.tar"])


def test_error_tar_folder_not_exists(change_to_temp_dir):
    with pytest.raises(FileNotFoundError, match="Папка не найдена"):
        tar_command(["fake", "test.tar.gz"])


def test_error_tar_source_is_file(change_to_temp_dir):
    with open("file.txt", "w") as f:
        f.write("content")
    with pytest.raises(ValueError, match="Не является папкой"):
        tar_command(["file.txt", "test.tar.gz"])


def test_tar_command_creates_archive(change_to_temp_dir):
    os.mkdir("docs")
    with open("docs/readme.md", "w") as f:
        f.write("zzzzz")
    tar_command(["docs", "docs.tar.gz"])
    assert os.path.exists("docs.tar.gz")
    import tarfile
    with tarfile.open("docs.tar.gz", "r:gz") as tf:
        members = tf.getnames()
        assert "docs" in members
        assert "docs/readme.md" in members


def test_untar_command_extracts_archive(change_to_temp_dir):
    import tarfile
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        docs_dir = os.path.join(tmpdir, "docs")
        os.mkdir(docs_dir)
        with open(os.path.join(docs_dir, "readme.md"), "w") as f:
            f.write("zzzz")
        with tarfile.open("test.tar.gz", "w:gz") as tf:
            tf.add(tmpdir, arcname="")
    untar_command(["test.tar.gz"])
    assert os.path.exists("docs")
    assert os.path.exists("docs/readme.md")


def test_error_untar_archive_not_exists():
    with pytest.raises(FileNotFoundError, match="Не удается найти указанный TAR"):
        untar_command(["fake.tar.gz"])


def test_error_untar_invalid_file(change_to_temp_dir):
    with open("fake.tar.gz", "w") as f:
        f.write("zzzzzz")
    with pytest.raises(ValueError, match="Не является TAR файлом"):
        untar_command(["fake.tar.gz"])
