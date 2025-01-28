from TraceTypes import Color, TextFormat, Label, Trace
from TraceBuilder import TraceBuilder
from Constants import start_keyword_skip_list, end_keyword_skip_list, newline_skip_list

from datetime import datetime
from shutil import get_terminal_size

class Logger:
    def __init__(self):
        self.trace_builder = TraceBuilder()
        self._print_legend()

    def suite_start(self, data, result) -> None:
        docs = data.doc.replace("\n", " ")
        print('=' * get_terminal_size().columns)
        print(f'Test suite: {data.name}\nDocumentation: {docs}')

    def suite_end(self, data, result) -> None:
        elapsed_time = self._compute_time_elapsed(result.starttime, result.endtime)
        color = Color.green if 'PASS' in result.status else Color.red
        print('=' * get_terminal_size().columns)
        print(f'Test suite finished in {elapsed_time} seconds\n'
              f'{result.statistics.total} executed,'
              f'{self._trace_to_str(Trace(color=Color.green.value, text=result.statistics.passed))} passed,'
              f'{self._trace_to_str(Trace(color=Color.red.value, text=result.statistics.failed))} failed,'
              f' {result.statistics.skipped} skipped\n'
              f'Suite result: {self._trace_to_str(Trace(color=color.value, text=result.status))}')

    def test_start(self, data, result) -> None:
        # to control the log indent for nested keyword calls
        self.curr_kw_lvl = 0
        self.prev_kw_lvl = 0
        docs = data.doc.replace("\n", " ")
        terminal_size = get_terminal_size()
        print('=' * terminal_size.columns)
        print(f'Test case: {data.name}\nDocumentation: {docs}')
        print('-' * terminal_size.columns)

    def test_end(self, data, result) -> None:
        color = Color.green if 'PASS' in result.status else Color.red
        time_elapsed = self._compute_time_elapsed(result.starttime, result.endtime)
        trace = self._trace_to_str(Trace(color=color.value, text=result.status))
        terminal_size = get_terminal_size()
        print('-' * terminal_size.columns)
        print(f'Test case finished in {time_elapsed} seconds\nTest result: {trace}')

    def keyword_start(self, data, implementation, result) -> None:
        if 'NOT RUN' not in result.status:
            if data.name not in start_keyword_skip_list:
                # print forwarded call label if the keyword is nested, else adjust indent
                label = f'{self._trace_to_str(Trace(label=Label.call.value))} ' if self.prev_kw_lvl < self.curr_kw_lvl else '  '
                indent = self.curr_kw_lvl * '\t'
                trace = self._trace_to_str(self.trace_builder.build_trace(data, implementation))
                terminator = '\n' if self._add_new_line(data) else ' '
                # if not in root keyword level, don't indent
                print((indent + label if self.curr_kw_lvl else '') + trace, end=terminator)
                self.prev_kw_lvl = self.curr_kw_lvl
            self.curr_kw_lvl += 1

    def keyword_end(self, data, implementation, result) -> None:
        if 'NOT RUN' not in result.status:
            self.curr_kw_lvl -= 1
            if data.name not in end_keyword_skip_list:
                label = Label.success.value if 'PASS' in result.status  else Label.fail.value
                indent = self.curr_kw_lvl * '\t'
                tab = '  ' if self.curr_kw_lvl else ''
                trace = self._trace_to_str(Trace(label=label, text=data.name))
                msg = ': ' + result.message if result.message else ''
                msg = self._trace_to_str(Trace(color=Color.red.value, text=msg))
                print(indent + tab + trace + msg)
        
    def _compute_time_elapsed(self, start_time, end_time) -> float:
        time_format = "%Y%m%d %H:%M:%S.%f"
        elapsed_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
        return elapsed_time.total_seconds()

    def _trace_to_str(self, msg: Trace) -> str:
        trace = ''
        for item in msg:
            trace += f'{str(item)} ' if item != '' else ''
        return trace[:-1] + TextFormat.clear.value
    
    def _add_new_line(self, data) -> bool:
        return data.name not in newline_skip_list
    
    def _print_legend(self) -> None:
        print(f'{self._trace_to_str(Trace(text="Robot Framework Pretty Logger"))}\n'
              f'{self._trace_to_str(Trace(text="Legend:"))} '
              f'{self._trace_to_str(Trace(label=Label.success.value, text="Pass"))} '
              f'{self._trace_to_str(Trace(label=Label.fail.value, text="Fail"))} '
              f'{self._trace_to_str(Trace(label=Label.busy.value, text="Running"))} '
              f'{self._trace_to_str(Trace(label=Label.call.value, text="Nested call"))}')