from datetime import datetime
from robot.api import logger
from Constants import *
import shutil

class CustomLogger:
    def __init__(self):
        logger.console(f'{italic}Robot Framework Fancy Logger{reset}\n'
                       f'{bold}Legend:{reset}\t'
                       f'✅ Pass\t'
                       f'❌ Fail\t'
                       f'⌛ Running')

    def suite_start(self, data, result) -> None:
        logger.console('=' * shutil.get_terminal_size().columns)
        logger.console(f'Test suite: {data.name}\nDocumentation: {data.doc}')

    def test_start(self, data, result) -> None:
        logger.console('-' * shutil.get_terminal_size().columns)
        logger.console(f'Test case: {data.name}\nDocumentation: {data.doc}')

    def test_end(self, data, result) -> None:
        elapsed_time = self.compute_time_elapsed(result.starttime, result.endtime)
        color = green if result.status == 'PASS' else red
        logger.console(f'Test case finished in {elapsed_time} seconds\n'
                       f'Result: {color}{italic}{result.status}{reset}')

    def suite_end(self, data, result) -> None:
        elapsed_time = self.compute_time_elapsed(result.starttime, result.endtime)
        color = green if result.status == 'PASS' else red
        logger.console(':' * shutil.get_terminal_size().columns)
        logger.console(f'Test suite finished in {elapsed_time} seconds\n'
                       f'Result: {color}{italic}{result.status}{reset}')

    def user_keyword_start(self, data, implementation, result) -> None:
        logger.console(f'⌛ {data.name}', newline=False)

    def user_keyword_end(self, data, implementation, result) -> None:
        marker = '✅' if result.status == 'PASS' else '❌'
        logger.console(f'\r{clear}{marker}{reset} {data.name}')

    def compute_time_elapsed(self, start_time, end_time) -> float:
        time_format = "%Y%m%d %H:%M:%S.%f"
        elapsed_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
        return elapsed_time.total_seconds()