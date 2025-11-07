import os
import zipfile
import tarfile


def zip_command(args: list[str]) -> None:
    """
    Создает zip файл.
    """
    if len(args) < 2:
        raise ValueError("Не указано имя архива или файла/папки")

    folder = args[0]
    archive_name = args[1]

    if not archive_name.endswith('.zip'):
        raise ValueError("Не является ZIP файлом.")

    if not os.path.exists(folder):
        raise FileNotFoundError("Папка не найдена")

    if not os.path.isdir(folder):
        raise ValueError("Не является папкой")

    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder)
                    zipf.write(file_path, arcname)

    except Exception:
        raise Exception("Непредвиденная ошибка при создании ZIP архива")


def unzip_command(args: list[str]) -> None:
    """
    Распаковывает zip файл.
    """
    if not args:
        raise ValueError("Не указан архив для распаковки")

    archive_name = args[0]
    destination = "."

    if not os.path.exists(archive_name):
        raise FileNotFoundError("Не удается найти указанный ZIP.")

    if not zipfile.is_zipfile(archive_name):
        raise ValueError("Не является ZIP файлом.")

    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            zipf.extractall(destination)

    except Exception:
        raise Exception("Непредвиденная ошибка при распаковки ZIP архива")


def tar_command(args: list[str]) -> None:
    """
    Создает tar файл.
    """
    if len(args) < 2:
        raise ValueError("Не указана папка и/или имя архива")

    folder = args[0]
    archive_name = args[1]

    if not archive_name.endswith('.tar.gz'):
        raise ValueError("Не является TAR.GZ файлом.")

    if not os.path.exists(folder):
        raise FileNotFoundError("Папка не найдена")

    if not os.path.isdir(folder):
        raise ValueError("Не является папкой")

    try:
        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add(folder, arcname=os.path.basename(folder))

    except Exception:
        raise Exception("Ошибка при создании TAR.GZ архива.")


def untar_command(args: list[str]) -> None:
    """
    Распаковывает tar файл.
    """
    if not args:
        raise ValueError("Не указан архив для распаковки")

    archive_name = args[0]
    destination = "."

    if not os.path.exists(archive_name):
        raise FileNotFoundError("Не удается найти указанный TAR.")

    if not tarfile.is_tarfile(archive_name):
        raise ValueError("Не является TAR файлом.")

    try:
        with tarfile.open(archive_name, 'r:gz') as tar:
            tar.extractall(destination)

    except Exception:
        raise Exception("Ошибка при распаковке TAR.GZ архива.")
