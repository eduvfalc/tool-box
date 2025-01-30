from os import path, mkdir, rmdir
from typing import Dict
import shutil
import json

from Constants import PATH_TO_OUTPUT
from Logger import Logger
from TraceTypes import *

from robot.running import TestSuite as TestSuiteData, TestCase as TestCaseData, Keyword as KeywordData, LibraryKeyword, UserKeyword
from robot.result import TestSuite as TestSuiteResult, TestCase as TestCaseResult, Keyword as KeywordResult

class Listener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.logger = Logger()

    def start_suite(self, data: TestSuiteData, result: TestSuiteResult):
        # create suite dir
        self.suite_name = data.name
        self.suite_dir = path.join(path.dirname(__file__), PATH_TO_OUTPUT + self.suite_name)
        self._create_dir(self.suite_dir)
        self.logger.suite_start(data, result)

    def start_test(self, data: TestCaseData, result: TestCaseResult):
        # create test dir
        self.test_dir = path.join(path.dirname(__file__), PATH_TO_OUTPUT + self.suite_name + "/" + data.name)
        self._create_dir(self.test_dir)
        self.logger.test_start(data, result)
    
    def end_suite(self, data: TestSuiteData, result: TestSuiteResult):
        # dump suite results
        self._dump_to_json(self.suite_dir + "/" + data.name, result.to_dict())
        self.logger.suite_end(data, result)

    def end_test(self, data: TestCaseData, result: TestCaseResult):
        # dump test results
        self._dump_to_json(self.test_dir + "/" + data.name, result.to_dict())
        self.logger.test_end(data, result)

    def start_user_keyword(self, data: KeywordData, implementation: UserKeyword, result: KeywordResult):
        self.logger.keyword_start(data, implementation, result)

    def end_user_keyword(self, data: KeywordData, implementation: UserKeyword, result: KeywordResult):
        self.logger.keyword_end(data, implementation, result)

    def start_library_keyword(self, data: KeywordData, implementation: LibraryKeyword, result: KeywordResult):
        self.logger.keyword_start(data, implementation, result)

    def end_library_keyword(self, data: KeywordData, implementation: LibraryKeyword, result: KeywordResult):
        self.logger.keyword_end(data, implementation, result)

    def _create_dir(self, dir: str):
        if (path.exists(dir)):
            shutil.rmtree(dir)
        mkdir(dir)

    def _dump_to_json(self, file: str, payload: Dict[str,any]):
        with open(file, 'w') as json_file:
            json.dump(payload, json_file, indent=4)