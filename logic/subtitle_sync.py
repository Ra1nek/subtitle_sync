import os

class SubtitleSync:
    def __init__(self):
        pass

    def process_subtitles(self, original_path, final_path, save_path, start_line, end_line):
        log_entries = []
        result_lines = []

        # Нормализация путей
        original_path = self.normalize_path(original_path)
        final_path = self.normalize_path(final_path)
        save_path = self.normalize_path(save_path)

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
            def read_subtitles(file_path):
                with open(file_path, 'r', encoding='utf-8-sig') as file:
                    return file.readlines()

            def write_subtitles(file_path, lines):
                with open(file_path, 'w', encoding='utf-8-sig') as file:
                    file.writelines(lines)

            def parse_subtitle_block(lines):
                block = []
                for line in lines:
                    line = line.strip()
                    if line:
                        block.append(line)
                    else:
                        if block:
                            yield block
                        block = []

            original_blocks = list(parse_subtitle_block(read_subtitles(original_path)))
            final_blocks = list(parse_subtitle_block(read_subtitles(final_path)))

            original_dict = {int(block[0]): block[1:] for block in original_blocks if block[0].isdigit()}
            final_dict = {int(block[0]): block[1:] for block in final_blocks if block[0].isdigit()}

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
                        result_lines.append(f"{line_number}\n")
                        result_lines.append(final_block[0] + "\n")
                        result_lines.extend(line + "\n" for line in final_block[1:])
                        result_lines.append("\n")
                        continue
                    
                    if len(orig_block) < 2:
                        log_entries.append(f"Ошибка в оригинальном файле: строка {line_number}: Не хватает данных.\n")
                        continue
                    
                    if len(final_block) < 2:
                        log_entries.append(f"Ошибка в конечном файле: строка {line_number}: Не хватает данных.\n")
                        continue
                    
                    if orig_block[0] == final_block[0]:
                        skipped_due_to_timing_match.append(line_number)
                        result_lines.append(f"{line_number}\n")
                        result_lines.append(final_block[0] + "\n")
                        result_lines.extend(line + "\n" for line in final_block[1:])
                    else:
                        result_lines.append(f"{line_number}\n")
                        result_lines.append(orig_block[0] + "\n")
                        result_lines.extend(line + "\n" for line in final_block[1:])
                        
                    result_lines.append("\n")
                    processed_lines += 1
                
                elif not orig_block:
                    missing_in_original.append(line_number)
                
                elif not final_block:
                    missing_in_final.append(line_number)

            for line_number in range(len(original_dict) + 1, len(final_blocks) + 1):
                final_block = final_dict.get(line_number)
                if final_block:
                    result_lines.append(f"{line_number}\n")
                    result_lines.append(final_block[0] + "\n")
                    result_lines.extend(line + "\n" for line in final_block[1:])
                    result_lines.append("\n")

            output_file_name = os.path.splitext(os.path.basename(final_path))[0] + '_resyns.srt'
            output_file_path = os.path.join(save_path, output_file_name)
            log_file_path = os.path.join(save_path, "log.txt")

            write_subtitles(output_file_path, result_lines)

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
            return log_entries, None

    def format_ranges(self, numbers):
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

    def normalize_path(self, path):
        if os.name == 'nt':
            return path.replace('/', '\\')
        else:
            return path.replace('\\', '/')
