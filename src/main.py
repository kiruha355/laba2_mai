import os
import sys
from src.logger import setup_logging
from src.commands.ls import ls_command
from src.commands.cd import cd_command
from src.commands.cat import cat_command
from src.commands.cp import cp_command
from src.commands.mv import mv_command
from src.commands.rm import rm_command
from src.commands.zip_and_tar import zip_command, unzip_command, tar_command, untar_command
from src.commands.grep import grep_command


class MiniShell:
    """
    Консоль файловых команд.
    """
    logger = setup_logging()
    commands = {
        "ls": ls_command,
        "cd": cd_command,
        "cat": cat_command,
        "cp": cp_command,
        "mv": mv_command,
        "rm": rm_command,
        "zip": zip_command,
        "unzip": unzip_command,
        "tar": tar_command,
        "untar": untar_command,
        "grep": grep_command
    }

    def run(self) -> None:
        """
        Запуск возможности ввода строки.
        """
        while True:
            try:
                user_input = input(f"{os.getcwd()}> ").strip()

                if not user_input:
                    self.logger.info("Ввод пустой строки")
                    continue

                if user_input == 'exit':
                    break

                self.logger.info(user_input)
                parts = user_input.split()
                command_name = parts[0]
                if len(parts) > 1:
                    args = parts[1:]
                else:
                    args = []

                if command_name in self.commands:
                    try:
                        command_function = self.commands[command_name]
                        result = command_function(args)
                        if result:
                            print(result)
                        self.logger.info("Success")
                    except Exception as error:
                        error_msg = str(error)
                        print(error_msg)
                        self.logger.error(error_msg)
                else:
                    error_msg = f"{command_name} не является внутренней или внешней командой, исполняемой программой или пакетным файлом."
                    print(error_msg)
                    self.logger.error(error_msg)

            except KeyboardInterrupt:
                self.logger.error("KeyboardInterrupt")
                sys.exit(0)


def main() -> None:
    """
    Запуск консоли.
    """
    launch = MiniShell()
    launch.run()


if __name__ == "__main__":
    main()
