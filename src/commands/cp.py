import os
import shutil


def cp_command(args: list[str]) -> None:
    """
    Копирование файла или каталога.
    """
    with_r = False
    source = None
    destination = None

    if len(args) >= 1 and args[0] == "-r":
        with_r = True
        if len(args) < 3:
            raise ValueError("Ошибка в синтаксисе команды.")
        source = args[1]
        destination = args[2]
    else:
        if len(args) < 2:
            raise ValueError("Невозможно скопировать файл поверх самого себя.")
        source = args[0]
        destination = args[1]

    if not os.path.exists(source):
        raise FileNotFoundError("Не удается найти указанный файл.")

    if os.path.isdir(source) and not with_r:
        raise ValueError("Не удается найти указанный файл.")

    try:
        if os.path.isfile(source):
            shutil.copy2(source, destination)
        elif os.path.isdir(source) and with_r:
            shutil.copytree(source, destination, dirs_exist_ok=True)

    except PermissionError:
        raise PermissionError(f"Нет прав доступа для копирования '{source}'.")

    except Exception:
        raise Exception("Невозможность копирования или нет права доступа у некоторых файлов.")
