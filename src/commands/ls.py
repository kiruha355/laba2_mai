import os
import datetime
import stat


def ls_command(args: list[str]) -> str:
    """
    Функция вывода содержимого каталога.
    """
    path = "."
    with_l = False

    for arg in args:
        if arg == "-l":
            with_l = True
        else:
            path = arg

    if os.path.isabs(path):
        actual_path = path
    else:
        actual_path = find_directory(path) or path

    if not os.path.exists(actual_path):
        raise FileNotFoundError(f"Путь '{actual_path}' не существует.")
    if not os.path.isdir(actual_path):
        raise NotADirectoryError(f"'{actual_path}' не является каталогом.")

    items = os.listdir(actual_path)

    if with_l:
        return get_list_with_l(actual_path, items)
    else:
        return "\n".join(items)


def find_directory(dir_name: str) -> str | None:
    """
    Ищет каталог по имени в текущей и родительских директориях.
    """
    current = os.getcwd()

    while True:
        check_path = os.path.join(current, dir_name)
        if os.path.isdir(check_path):
            return check_path

        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    return None


def get_list_with_l(path: str, items: list[str]) -> str:
    """
    Показывает детальную информацию о файлах.
    """
    result = []

    for item in items:
        full_path = os.path.join(path, item)
        stat_info = os.stat(full_path)

        result.append(
            f"{stat.filemode(stat_info.st_mode)} "
            f"{stat_info.st_size:8} "
            f"{datetime.datetime.fromtimestamp(stat_info.st_mtime):%Y-%m-%d %H:%M} "
            f"{item}{'/' if os.path.isdir(full_path) else ''}"
        )

    return "\n".join(result)
