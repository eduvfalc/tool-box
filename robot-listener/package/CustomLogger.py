from datetime import datetime
from robot.api import logger
from Constants import *
import shutil

class CustomLogger:
    def __init__(self, overwrite_keyword_logs:bool):
        self.insert_newline = not overwrite_keyword_logs
        logger.console(f'{cyan}Robot Framework Pretty Logger{reset}\n'
                       f'{bold}Legend:{reset}\t'
                       f'✅ Pass\t'
                       f'❌ Fail\t'
                       f'⌛ Running')

    def suite_start(self, data, result) -> None:
        docs = data.doc.replace("\n", " ")
        logger.console('=' * shutil.get_terminal_size().columns)
        logger.console(f'Test suite: {data.name}\nDocumentation: {docs}')

    def test_start(self, data, result) -> None:
        docs = data.doc.replace("\n", " ")
        logger.console('-' * shutil.get_terminal_size().columns)
        logger.console(f'Test case: {data.name}\n'
                       f'Documentation: {docs}\n'
                       f'\n{bold}Start{reset}')

    def test_end(self, data, result) -> None:
        elapsed_time = self.compute_time_elapsed(result.starttime, result.endtime)
        color = green if result.status == 'PASS' else red
        logger.console(f'{bold}End{reset}\n\n'
                       f'Test case finished in {elapsed_time} seconds\n'
                       f'Result: {color}{italic}{result.status}{reset}')

    def suite_end(self, data, result) -> None:
        elapsed_time = self.compute_time_elapsed(result.starttime, result.endtime)
        color = green if result.status == 'PASS' else red
        logger.console(':' * shutil.get_terminal_size().columns)
        logger.console(f'Test suite finished in {elapsed_time} seconds\n'
                       f'Result: {color}{italic}{result.status}{reset}')

    def user_keyword_start(self, data, implementation, result) -> None:
        logger.console(f'⌛ {data.name}', newline=self.insert_newline)

    def user_keyword_end(self, data, implementation, result) -> None:
        marker = '✅' if result.status == 'PASS' else '❌'
        message = ': ' + result.message if result.message else ''
        logger.console(f'\r{clear}{marker}{reset} {data.name}{message}')

    def compute_time_elapsed(self, start_time, end_time) -> float:
        time_format = "%Y%m%d %H:%M:%S.%f"
        elapsed_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
        return elapsed_time.total_seconds()