import os
import re


def grep_command(args: list[str]) -> str:
    """
    Поиск по файловому содержимому.
    """
    if len(args) < 2:
        raise ValueError("Не указан шаблон или путь")

    with_r = False
    with_i = False

    if args[0] in ("-ri", "-ir"):
        with_r = True
        with_i = True
        actual_args = args[1:]
    elif args[0] == "-r":
        with_r = True
        actual_args = args[1:]
    elif args[0] == "-i":
        with_i = True
        actual_args = args[1:]
    else:
        actual_args = args

    pattern, path = actual_args[0], actual_args[1]

    results: list[tuple[str, int, str]] = []
    flags = re.IGNORECASE if with_i else 0

    if os.path.isfile(path):
        search_file(path, pattern, flags, results)
    elif os.path.isdir(path):
        if with_r:
            for root, dirs, files in os.walk(path):
                for file in files:
                    search_file(os.path.join(root, file), pattern, flags, results)
        else:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    search_file(item_path, pattern, flags, results)
    else:
        raise FileNotFoundError("Пути не существует")

    if not results:
        return "Совпадений не найдено"

    return "\n".join(f"{file}:{line_num}:{line.strip()}" for file, line_num, line in results)


def search_file(file_path: str, pattern: str, flags: int, results: list[tuple[str, int, str]]) -> None:
    """
    Поиск в файле.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                if re.search(pattern, line, flags):
                    results.append((file_path, line_num, line))
    except Exception:
        raise Exception("Ошибка при чтении файла.")
