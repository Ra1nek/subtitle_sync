# logic/subtitle_sync.py

import os
import logging
from .file_handler import FileHandler

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SubtitleSync:
    def __init__(self):
        self.file_handler = FileHandler()

    def process_subtitles(self, original_path, final_path, save_path, start_line, end_line):
        """
        Обработка субтитров.
        """
        log_entries = []
        result_lines = []

        # Нормализация путей
        original_path = self.file_handler.normalize_path(original_path)
        final_path = self.file_handler.normalize_path(final_path)
        save_path = self.file_handler.normalize_path(save_path)

        if not original_path or not final_path or not save_path:
            error_msg = "Пожалуйста, выберите все необходимые файлы и папки."
            log_entries.append(f"Ошибка: {error_msg}\n")
            return log_entries, None

        try:
            start_line = int(start_line) if start_line else None
            end_line = int(end_line) if end_line else None
        except ValueError:
            error_msg = "Введите допустимые номера строк для обработки."
            log_entries.append(f"Ошибка: {error_msg}\n")
            return log_entries, None

        try:
            original_blocks = self.read_and_parse_subtitles(original_path)
            final_blocks = self.read_and_parse_subtitles(final_path)

            original_dict = self.create_subtitle_dict(original_blocks)
            final_dict = self.create_subtitle_dict(final_blocks)

            max_line_number = max(len(original_dict), len(final_dict))

            skipped_due_to_timing_match = []
            missing_in_original = []
            missing_in_final = []
            processed_lines = 0

            for line_number in range(1, max_line_number + 1):
                orig_block = original_dict.get(line_number)
                final_block = final_dict.get(line_number)

                if orig_block and final_block:
                    if start_line and end_line and (line_number < start_line or line_number > end_line):
                        result_lines.extend(self.format_subtitle_block(line_number, final_block))
                        continue

                    if len(orig_block) < 2:
                        log_entries.append(f"Ошибка в оригинальном файле: строка {line_number}: Не хватает данных.\n")
                        continue

                    if len(final_block) < 2:
                        log_entries.append(f"Ошибка в конечном файле: строка {line_number}: Не хватает данных.\n")
                        continue

                    if orig_block[0] == final_block[0]:
                        skipped_due_to_timing_match.append(line_number)
                        result_lines.extend(self.format_subtitle_block(line_number, final_block))
                    else:
                        result_lines.extend(self.format_subtitle_block(line_number, orig_block, final_block[1:]))

                    result_lines.append("\n")
                    processed_lines += 1

                elif not orig_block:
                    missing_in_original.append(line_number)

                elif not final_block:
                    missing_in_final.append(line_number)

            for line_number in range(len(original_dict) + 1, len(final_blocks) + 1):
                final_block = final_dict.get(line_number)
                if final_block:
                    result_lines.extend(self.format_subtitle_block(line_number, final_block))
                    result_lines.append("\n")

            output_file_name = os.path.splitext(os.path.basename(final_path))[0] + '_resyns.srt'
            output_file_path = os.path.join(save_path, output_file_name)
            log_file_path = os.path.join(save_path, "log.txt")

            self.file_handler.write_file(output_file_path, result_lines)

            with open(log_file_path, 'w', encoding='utf-8-sig') as log_file:
                if skipped_due_to_timing_match:
                    log_entries.append(f"Не обработаны строки из-за совпадения тайминга: {self.format_ranges(skipped_due_to_timing_match)}\n")

                if missing_in_original:
                    log_entries.append(f"Отсутствуют строки в оригинальном файле: {self.format_ranges(missing_in_original)}\n")
                if missing_in_final:
                    log_entries.append(f"Отсутствуют строки в конечном файле: {self.format_ranges(missing_in_final)}\n")

                log_file.writelines(log_entries)

            return log_entries, output_file_path

        except Exception as e:
            error_msg = f"Произошла ошибка: {str(e)}"
            log_entries.append(f"Ошибка: {error_msg}\n")
            logging.error(error_msg)
            return log_entries, None

    def read_and_parse_subtitles(self, file_path):
        """
        Чтение и парсинг субтитров из файла.
        """
        lines = self.file_handler.read_file(file_path)
        return list(self.parse_subtitle_block(lines))

    def parse_subtitle_block(self, lines):
        """
        Парсинг блоков субтитров.
        """
        block = []
        for line in lines:
            line = line.strip()
            if line:
                block.append(line)
            else:
                if block:
                    yield block
                block = []

    def create_subtitle_dict(self, blocks):
        """
        Создание словаря субтитров.
        """
        return {int(block[0]): block[1:] for block in blocks if block[0].isdigit()}

    def format_subtitle_block(self, line_number, *blocks):
        """
        Форматирование блока субтитров.
        """
        formatted_block = [f"{line_number}\n"]
        for block in blocks:
            formatted_block.extend(line + "\n" for line in block)
        return formatted_block

    def format_ranges(self, numbers):
        """
        Форматирование диапазонов номеров.
        """
        if not numbers:
            return ""
        ranges = []
        start = prev = numbers[0]

        for number in numbers[1:]:
            if number == prev + 1:
                prev = number
            else:
                if start == prev:
                    ranges.append(f"{start}")
                else:
                    ranges.append(f"{start}-{prev}")
                start = prev = number
        if start == prev:
            ranges.append(f"{start}")
        else:
            ranges.append(f"{start}-{prev}")

        return ', '.join(ranges)
