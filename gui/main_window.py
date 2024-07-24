from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.uic import loadUi
import os
from logic.subtitle_sync import SubtitleSync

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('resources/main_window.ui', self)

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
        font_db = QFontDatabase()
        font_path = 'resources/fonts/SegoeUI.ttf'
        font_id = font_db.addApplicationFont(font_path)
        if font_id != -1:
            font_family = font_db.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 9)  # Устанавливаем размер шрифта в 9 пунктов
            self.setFont(font)
        else:
            print("Не удалось загрузить шрифт.")

    def apply_stylesheet(self):
        stylesheet_path = 'resources/style.qss'
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r') as file:
                self.setStyleSheet(file.read())
        else:
            print("Не удалось найти файл стиля.")

    def select_original_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выберите оригинальный файл субтитров", "", "SubRip Subtitle files (*.srt)")
        if file:
            self.originalFilePath.setText(self.normalize_path(file))

    def select_final_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выберите конечный файл субтитров", "", "SubRip Subtitle files (*.srt)")
        if file:
            self.finalFilePath.setText(self.normalize_path(file))

    def select_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения результата")
        if folder:
            folder = self.normalize_path(folder)
            if not folder.endswith(os.sep):
                folder += os.sep
            self.savePath.setText(folder)

    def process_subtitles(self):
        original_path = self.originalFilePath.text()
        final_path = self.finalFilePath.text()
        save_path = self.savePath.text()
        start_line = self.startLineEdit.text()
        end_line = self.endLineEdit.text()

        log_entries, output_file_path = self.subtitle_sync.process_subtitles(
            original_path, final_path, save_path, start_line, end_line
        )

        if log_entries:
            log_message = "Обработка завершена! "
            if output_file_path:
                log_message += f"Результат сохранен в {output_file_path}\n"
            log_message += f"Лог записан в {self.normalize_path(save_path)}log.txt"
            QMessageBox.information(self, "Информация", log_message)

    def normalize_path(self, path):
        if os.name == 'nt':
            return path.replace('/', '\\')
        else:
            return path.replace('\\', '/')
