import os


def cat_command(args: list[str]) -> str:
    """
    Показывает содержимое файла.
    """
    if not args:
        raise ValueError("Ошибка в синтаксисе команды.")

    filename = args[0]

    if not os.path.exists(filename):
        raise FileNotFoundError("Не удается найти указанный файл.")

    if os.path.isdir(filename):
        raise IsADirectoryError("Отказано в доступе.")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return content

    except UnicodeDecodeError:
        raise ValueError(f"Файл '{filename}' не является текстовым файлом.")

    except PermissionError:
        raise PermissionError(f"Нет доступа к файлу '{filename}'.")

    except Exception:
        raise Exception("Ошибка при чтении файла.")
