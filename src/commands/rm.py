import os
import shutil


def rm_command(args: list[str]) -> None:
    """
    Удаление файла или каталога.
    """
    if not args:
        raise ValueError("Ошибка в синтаксисе команды.")

    with_r = False
    file_or_folder = args[0]

    if args[0] == "-r":
        if len(args) < 2:
            raise ValueError("Не удается найти -r")
        with_r = True
        file_or_folder = args[1]

    if not os.path.exists(file_or_folder):
        raise FileNotFoundError("Не удается найти указанный файл\папку.")

    abs_path = os.path.abspath(file_or_folder)
    root_path = os.path.abspath("/")
    parent_path = os.path.abspath("..")

    if abs_path == root_path or abs_path == parent_path:
        raise ValueError("Запрещено удалять корневой или родительский каталог")

    try:
        if os.path.isfile(file_or_folder):
            os.remove(file_or_folder)

        elif os.path.isdir(file_or_folder):
            if not with_r:
                raise ValueError(f"'{file_or_folder}' является каталогом.")

            print(f"Вы уверены, что хотите удалить каталог '{file_or_folder}'?")
            response = input("[Y(yes)/N(no)]")

            if response in ["y", "Y"]:
                shutil.rmtree(file_or_folder)

    except PermissionError:
        raise PermissionError(f"Нет прав доступа для удаления '{file_or_folder}'")
