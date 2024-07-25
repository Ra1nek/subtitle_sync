# logic/file_handler.py

import os

class FileHandler:
    def __init__(self):
        pass

    def read_file(self, file_path):
        """
        Чтение содержимого файла.

        Args:
            file_path (str): Путь к файлу.

        Returns:
            list: Список строк из файла.
        """
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return file.readlines()

    def write_file(self, file_path, lines):
        """
        Запись содержимого в файл.

        Args:
            file_path (str): Путь к файлу.
            lines (list): Список строк для записи.
        """
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.writelines(lines)

    def normalize_path(self, path):
        """
        Нормализация пути в зависимости от операционной системы.

        Args:
            path (str): Путь.

        Returns:
            str: Нормализованный путь.
        """
        if os.name == 'nt':
            return path.replace('/', '\\')
        else:
            return path.replace('\\', '/')
