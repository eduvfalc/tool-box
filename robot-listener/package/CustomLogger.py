from datetime import datetime
from robot.api import logger
from CustomTypes import *
import shutil

class CustomLogger:
    def __init__(self, overwrite_keyword_logs: bool):
        self.keyword_lvl = 0
        self.overwrite_kw_logs = overwrite_keyword_logs
        print(f'{self._create_trace(Trace(text="Robot Framework Pretty Logger"))}\n'
              f'{self._create_trace(Trace(text="Legend:"))} '
              f'{self._create_trace(Trace(label=Label.success.value, text="Pass"))} '
              f'{self._create_trace(Trace(label=Label.fail.value, text="Fail"))} '
              f'{self._create_trace(Trace(label=Label.busy.value, text="Running"))} '
              f'{self._create_trace(Trace(label=Label.call.value, text="Nested call"))}')

    def suite_start(self, data, result) -> None:
        docs = data.doc.replace("\n", " ")
        print('=' * shutil.get_terminal_size().columns)
        print(f'Test suite: {data.name}\nDocumentation: {docs}')

    def suite_end(self, data, result) -> None:
        elapsed_time = self.compute_time_elapsed(result.starttime, result.endtime)
        color = Color.green if 'PASS' in result.status else Color.red
        print('=' * shutil.get_terminal_size().columns)
        print(f'Test suite finished in {elapsed_time} seconds\n'
              f'{result.statistics.total} executed, '
              f'{self._create_trace(Trace(color=Color.green.value, text=result.statistics.passed))} passed, '
              f'{self._create_trace(Trace(color=Color.red.value, text=result.statistics.failed))} failed, '
              f'{result.statistics.skipped} skipped\n'
              f'Suite result: {self._create_trace(Trace(color=color.value, text=result.status))}')

    def test_start(self, data, result) -> None:
        self.keyword_lvl = 0
        docs = data.doc.replace("\n", " ")
        print('=' * shutil.get_terminal_size().columns)
        print(f'Test case: {data.name}\n'
              f'Documentation: {docs}')
        print('-' * shutil.get_terminal_size().columns)

    def test_end(self, data, result) -> None:
        print('-' * shutil.get_terminal_size().columns)
        elapsed_time = self.compute_time_elapsed(result.starttime, result.endtime)
        color = Color.green if 'PASS' in result.status else Color.red
        print(f'Test case finished in {elapsed_time} seconds\n'
              f'Test result: {self._create_trace(Trace(color=color.value, text=result.status))}')

    def keyword_start(self, data, implementation, result) -> None:
        if 'NOT RUN' not in result.status:
            print(self.keyword_lvl * '\t' + (f'{self._create_trace(Trace(label=Label.call.value))} ' if self.keyword_lvl else '') \
                                            + f'{self._create_trace(Trace(label=Label.busy.value, text=data.name))}')
            self.keyword_lvl += 1

    def keyword_end(self, data, implementation, result) -> None:
        if 'NOT RUN' not in result.status:
            self.keyword_lvl -= 1
            label = Label.success.value if 'PASS' in result.status  else Label.fail.value
            message = ': ' + result.message if result.message else ''
            print(self.keyword_lvl * '\t' + f'{self._create_trace(Trace(label=label, text=data.name))}{message}')
        
    def compute_time_elapsed(self, start_time, end_time) -> float:
        time_format = "%Y%m%d %H:%M:%S.%f"
        elapsed_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
        return elapsed_time.total_seconds()

    def _create_trace(self, msg: Trace) -> str:
        return f'{msg.label}{msg.color}{msg.text}{Color.reset.value}'