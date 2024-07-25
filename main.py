import sys
import logging
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Основная функция для запуска приложения.
    """
    try:
        app = QApplication(sys.argv)
        main_win = MainWindow()
        main_win.show()
        logging.info("Приложение запущено успешно.")
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Ошибка при запуске приложения: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
