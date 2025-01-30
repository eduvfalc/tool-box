from shutil import get_terminal_size
from datetime import datetime
from typing import Union

from Constants import start_keyword_skip_list, end_keyword_skip_list, newline_skip_list
from TraceTypes import Color, Label, Trace
from TraceBuilder import TraceBuilder

from robot.running import TestSuite as TestSuiteData, TestCase as TestCaseData, Keyword as KeywordData, LibraryKeyword, UserKeyword
from robot.result import TestSuite as TestSuiteResult, TestCase as TestCaseResult, Keyword as KeywordResult

class Logger:
    def __init__(self):
        self.trace_builder = TraceBuilder()
        self._print_legend()

    def suite_start(self, data: TestSuiteData, result: TestSuiteResult) -> None:
        docs = data.doc.replace("\n", " ")
        print('=' * get_terminal_size().columns)
        print(f'Test suite: {data.name}\nDocumentation: {docs}')

    def suite_end(self, data: TestSuiteData, result: TestSuiteResult) -> None:
        elapsed_time = self._compute_time_elapsed(result.starttime, result.endtime)
        color = Color.green if 'PASS' in result.status else Color.red
        print('=' * get_terminal_size().columns)
        print(f'Test suite finished in {elapsed_time} seconds\n'
              f'{result.statistics.total} executed,'
              f'{Trace(color=Color.green.value, text=result.statistics.passed).to_str()} passed,'
              f'{Trace(color=Color.red.value, text=result.statistics.failed).to_str()} failed,'
              f'{result.statistics.skipped} skipped\n'
              f'Suite result: {Trace(color=color.value, text=result.status).to_str()}')

    def test_start(self, data: TestCaseData, result: TestCaseResult) -> None:
        # to control the log indent for nested keyword calls
        self.curr_kw_lvl = 0
        self.prev_kw_lvl = 0
        docs = data.doc.replace("\n", " ")
        terminal_size = get_terminal_size()
        print('=' * terminal_size.columns)
        print(f'Test case: {data.name}\nDocumentation: {docs}')
        print('-' * terminal_size.columns)

    def test_end(self, data: TestCaseData, result: TestCaseResult) -> None:
        color = Color.green if 'PASS' in result.status else Color.red
        time_elapsed = self._compute_time_elapsed(result.starttime, result.endtime)
        trace = Trace(color=color.value, text=result.status).to_str()
        terminal_size = get_terminal_size()
        print('-' * terminal_size.columns)
        print(f'Test case finished in {time_elapsed} seconds\nTest result: {trace}')

    def keyword_start(self, data: KeywordData, implementation: Union[UserKeyword, LibraryKeyword], result: KeywordResult) -> None:
        if 'NOT RUN' not in result.status and data.name not in start_keyword_skip_list:
            # print forwarded call label if the keyword is nested, else adjust indent
            label = f'{Trace(label=Label.call.value).to_str()} ' if self.prev_kw_lvl < self.curr_kw_lvl else '  '
            indent = self.curr_kw_lvl * '\t'
            trace = self.trace_builder.build_trace(data, implementation).to_str()
            terminator = '\n' if data.name not in newline_skip_list else ' '
            # if not in root keyword level, don't indent
            print((indent + label if self.curr_kw_lvl else '') + trace, end=terminator)
            self.prev_kw_lvl = self.curr_kw_lvl
        self.curr_kw_lvl += 1

    def keyword_end(self, data: KeywordData, implementation: Union[UserKeyword, LibraryKeyword], result: KeywordResult) -> None:
        self.curr_kw_lvl -= 1
        if 'NOT RUN' not in result.status and data.name not in end_keyword_skip_list:
            label = Label.success.value if 'PASS' in result.status  else Label.fail.value
            indent = self.curr_kw_lvl * '\t'
            tab = '  ' if self.curr_kw_lvl else ''
            trace = Trace(label=label, text=data.name).to_str()
            msg = ': ' + result.message if result.message else ''
            msg = Trace(color=Color.red.value, text=msg).to_str()
            print(indent + tab + trace + msg)
        
    def _compute_time_elapsed(self, start_time, end_time) -> float:
        time_format = "%Y%m%d %H:%M:%S.%f"
        elapsed_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
        return elapsed_time.total_seconds()
    
    def _print_legend(self) -> None:
        print(f'{Trace(text="Robot Framework Pretty Logger").to_str()}\n'
              f'{Trace(text="Legend:").to_str()} '
              f'{Trace(label=Label.success.value, text="Pass").to_str()} '
              f'{Trace(label=Label.fail.value, text="Fail").to_str()} '
              f'{Trace(label=Label.busy.value, text="Running").to_str()} '
              f'{Trace(label=Label.call.value, text="Nested call").to_str()}')