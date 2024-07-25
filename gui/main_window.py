# gui/main_window.py

import os
import logging
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.uic import loadUi
from logic.subtitle_sync import SubtitleSync
from config import RESOURCES_PATH, FONTS_PATH, STYLES_PATH

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(RESOURCES_PATH + 'main_window.ui', self)

        # Загрузка шрифта
        self.load_font()

        # Применение стиля
        self.apply_stylesheet()

        # Создаем экземпляр SubtitleSync
        self.subtitle_sync = SubtitleSync()

        # Подключаем события
        self.selectOriginalButton.clicked.connect(self.select_original_file)
        self.selectFinalButton.clicked.connect(self.select_final_file)
        self.selectSavePathButton.clicked.connect(self.select_save_folder)
        self.processButton.clicked.connect(self.process_subtitles)

    def load_font(self):
        """
        Загрузка шрифта из файла.
        """
        font_db = QFontDatabase()
        font_path = FONTS_PATH + 'SegoeUI.ttf'
        font_id = font_db.addApplicationFont(font_path)
        if font_id != -1:
            font_family = font_db.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 9)  # Устанавливаем размер шрифта в 9 пунктов
            self.setFont(font)
        else:
            logging.error("Не удалось загрузить шрифт.")

    def apply_stylesheet(self):
        """
        Применение стиля из файла.
        """
        if os.path.exists(STYLES_PATH):
            with open(STYLES_PATH, 'r') as file:
                self.setStyleSheet(file.read())
        else:
            logging.error("Не удалось найти файл стиля.")

    def select_original_file(self):
        """
        Выбор оригинального файла субтитров.
        """
        file, _ = QFileDialog.getOpenFileName(self, "Выберите оригинальный файл субтитров", "", "SubRip Subtitle files (*.srt)")
        if file:
            self.originalFilePath.setText(self.normalize_path(file))

    def select_final_file(self):
        """
        Выбор конечного файла субтитров.
        """
        file, _ = QFileDialog.getOpenFileName(self, "Выберите конечный файл субтитров", "", "SubRip Subtitle files (*.srt)")
        if file:
            self.finalFilePath.setText(self.normalize_path(file))

    def select_save_folder(self):
        """
        Выбор папки для сохранения результата.
        """
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения результата")
        if folder:
            folder = self.normalize_path(folder)
            if not folder.endswith(os.sep):
                folder += os.sep
            self.savePath.setText(folder)

    def process_subtitles(self):
        """
        Обработка субтитров.
        """
        original_path = self.originalFilePath.text()
        final_path = self.finalFilePath.text()
        save_path = self.savePath.text()
        start_line = self.startLineEdit.text()
        end_line = self.endLineEdit.text()

        try:
            log_entries, output_file_path = self.subtitle_sync.process_subtitles(
                original_path, final_path, save_path, start_line, end_line
            )

            if log_entries:
                log_message = "Обработка завершена! "
                if output_file_path:
                    log_message += f"Результат сохранен в {output_file_path}\n"
                log_message += f"Лог записан в {self.normalize_path(save_path)}log.txt"
                QMessageBox.information(self, "Информация", log_message)
        except Exception as e:
            logging.error(f"Ошибка при обработке субтитров: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обработке субтитров: {e}")

    def normalize_path(self, path):
        """
        Нормализация пути в зависимости от операционной системы.
        """
        if os.name == 'nt':
            return path.replace('/', '\\')
        else:
            return path.replace('\\', '/')
