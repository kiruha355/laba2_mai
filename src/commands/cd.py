import os


def cd_command(args: list[str]) -> str:
    """
    Функция перехода по каталогам.
    """
    if not args:
        target_path = os.path.expanduser("~")
    else:
        target_path = args[0]

    if target_path == "~":
        target_path = os.path.expanduser("~")
    elif target_path == "..":
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        target_path = parent_dir if parent_dir != current_dir else current_dir
    elif target_path == ".":
        target_path = os.getcwd()
    elif target_path.startswith("~"):
        target_path = os.path.expanduser(target_path)

    try:
        os.chdir(target_path)
        return os.getcwd()
    except FileNotFoundError:
        raise FileNotFoundError("Системе не удается найти указанный путь.")
