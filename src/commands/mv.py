import os
import shutil


def mv_command(args: list[str]) -> None:
    """
    Перемещает файлы или каталоги в указанное место.Переименовывает файлы.
    """
    if len(args) < 2:
        raise ValueError("Ошибка в синтаксисе команды.")

    if len(args) == 2:
        return single_mv(args[0], args[1])
    else:
        return multiple_mv(args[:-1], args[-1])


def single_mv(source: str, destination: str) -> None:
    """
    Перемещает/переименовывает один файл или каталог.
    """
    if not os.path.exists(source):
        raise FileNotFoundError("Не удается найти указанный файл.")

    if os.path.isdir(destination):
        filename = os.path.basename(source)
        destination_path = os.path.join(destination, filename)
    else:
        destination_path = destination

    try:
        shutil.move(source, destination_path)

    except PermissionError:
        raise PermissionError(f"Нет прав доступа для перемещения '{source}'")
    except Exception:
        raise Exception("Ошибка при перемещении.")


def multiple_mv(sources: list[str], destination_dir: str) -> None:
    """
    Перемещает несколько файлов или каталогов в указанную папку.
    """
    if not os.path.exists(destination_dir):
        raise FileNotFoundError("Не удается найти указанный файл.")

    if not os.path.isdir(destination_dir):
        raise ValueError("Назначение не является папкой.")

    for source in sources:
        if not os.path.exists(source):
            raise FileNotFoundError("Не удается найти указанный файл.")

    for source in sources:
        try:
            filename = os.path.basename(source)
            destination_path = os.path.join(destination_dir, filename)
            shutil.move(source, destination_path)

        except PermissionError:
            raise PermissionError(f"Нет прав доступа для перемещения '{source}'")
        except Exception:
            raise Exception("Ошибка при перемещении.")
