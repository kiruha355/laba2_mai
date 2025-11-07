import os
import pytest
from src.commands.grep import grep_command


def test_error_no_args():
    with pytest.raises(ValueError, match="Не указан шаблон или путь"):
        grep_command([])


def test_error_file_not_exists():
    with pytest.raises(FileNotFoundError, match="Пути не существует"):
        grep_command(["test", "nonexist.txt"])


def test_match(change_to_temp_dir):
    with open("file.txt", "w", encoding="utf-8") as f:
        f.write("mama")

    result = grep_command(["mama", "file.txt"])
    assert "file.txt:1:mama" in result


def test_no_match(change_to_temp_dir):
    with open("file.txt", "w", encoding="utf-8") as f:
        f.write("erm")

    result = grep_command(["hmm", "file.txt"])
    assert result == "Совпадений не найдено"


def test_grep_case_sensitive(change_to_temp_dir):
    with open("data.txt", "w", encoding="utf-8") as f:
        f.write("Z")

    result = grep_command(["z", "data.txt"])
    assert result == "Совпадений не найдено"


def test_insensitive(change_to_temp_dir):
    with open("data.txt", "w", encoding="utf-8") as f:
        f.write("z\nZ")

    result = grep_command(["-i", "z", "data.txt"])
    lines = result.splitlines()
    assert len(lines) == 2
    assert "z" in result
    assert "Z" in result


def test_grep_directory_without_r(change_to_temp_dir):
    with open("file1.txt", "w", encoding="utf-8") as f:
        f.write("match in root\n")
    os.mkdir("test_folder")
    with open("test_folder/file2.txt", "w", encoding="utf-8") as f:
        f.write("z")

    result = grep_command(["match", "."])
    assert "file1.txt:1:match in root" in result
    assert "test_folder" not in result


def test_directory_with_r(change_to_temp_dir):
    with open("file.txt", "w", encoding="utf-8") as f:
        f.write("meow here")

    os.mkdir("dir")
    with open("dir/file.txt", "w", encoding="utf-8") as f:
        f.write("meow there")

    result = grep_command(["-r", "meow", "."])
    lines = result.splitlines()
    assert len(lines) == 2
    assert any("file.txt" in line for line in lines)
    assert any("dir" in line for line in lines)


def test_error_directory_with_ri_flags(change_to_temp_dir):
    os.mkdir("search_dir")
    with open("search_dir/file.txt", "w", encoding="utf-8") as f:
        f.write("HM")

    result = grep_command(["-ri", "hm", "."])
    lines = result.splitlines()
    assert len(lines) == 1
    parts = lines[0].split(":", 2)
    assert len(parts) == 3
    file_path, line_num, content = parts

    assert os.path.basename(file_path) == "file.txt"
    assert line_num == "1"
    assert content.strip() == "HM"
    assert "search_dir" in file_path


def test_error_not_text_file(change_to_temp_dir, monkeypatch):
    with open("binary.bin", "wb") as f:
        f.write(b"\xFF\xFE")

    original_open = open

    def mock_open(path, *args, **kwargs):
        if path.endswith("binary.bin"):
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(Exception, match="Ошибка при чтении файла"):
        grep_command(["test", "binary.bin"])
