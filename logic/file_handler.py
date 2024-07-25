import os

class FileHandler:
    def __init__(self):
        pass

    def read_file(self, file_path):
        """
        Чтение содержимого файла.
        """
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return file.readlines()

    def write_file(self, file_path, lines):
        """
        Запись содержимого в файл.
        """
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.writelines(lines)

    def normalize_path(self, path):
        """
        Нормализация пути в зависимости от операционной системы.
        """
        if os.name == 'nt':
            return path.replace('/', '\\')
        else:
            return path.replace('\\', '/')
