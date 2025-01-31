from TraceTypes import Label, Trace
from robot.libraries.BuiltIn import BuiltIn

class TraceBuilder:
    def __init__(self):
        self.built_in = BuiltIn()

    def build_trace(self, data, implementation):
        return Trace(label=self._add_label(data), \
                     color=self._add_color(data), \
                     text=self._add_text(data, implementation), \
                     text_format=self._add_text_format(data))

    def _add_label(self, data):
        match data.name:
            case _ if "Log" in data.name:
                return Label.log.value
            case _ if "Sleep" in data.name:
                return Label.sleep.value
            case _:
                return Label.busy.value

    def _add_color(self, data):
        # TODO: add color for different keywords
        match data.name:
            case _:
                return ''
    
    def _add_text_format(self, data):
        # TODO: add text format for different keywords
        match data.name:
            case _:
                return ''
            
    def _add_text(self, data, implementation):
        match data.name:
            case _ if data.name == "Log":
                return self.built_in.replace_variables(data.args[0])
            case _ if data.name == "Log To Console":
                return ''
            case _ if data.name == "Log Many":
                return self.built_in.replace_variables(data.args[0])
            case _ if data.name == "Sleep":
                return f'{data.name} {data.args[0]}'
            case _:
                return data.name