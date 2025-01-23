from os import path, mkdir, rmdir
from Logger import Logger
from TraceTypes import *
import shutil
import json

# path to out folder
PATH_TO_OUTPUT = "../out/"

class Listener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.logger = Logger()

    def start_suite(self, data, result):
        # create suite dir
        self.suite_name = data.name
        self.suite_dir = path.join(path.dirname(__file__), PATH_TO_OUTPUT + self.suite_name)
        self.create_dir(self.suite_dir)
        self.logger.suite_start(data, result)

    def start_test(self, data, result):
        # create test dir
        self.test_dir = path.join(path.dirname(__file__), PATH_TO_OUTPUT + self.suite_name + "/" + data.name)
        self.create_dir(self.test_dir)
        self.logger.test_start(data, result)
    
    def end_suite(self, data, result):
        # dump suite results
        self.dump_to_json(self.suite_dir + "/" + data.name, result.to_dict())
        self.logger.suite_end(data, result)

    def end_test(self, data, result):
        # dump test results
        self.dump_to_json(self.test_dir + "/" + data.name, result.to_dict())
        self.logger.test_end(data, result)

    def start_user_keyword(self, data, implementation, result):
        self.logger.keyword_start(data, implementation, result)

    def end_user_keyword(self, data, implementation, result):
        self.logger.keyword_end(data, implementation, result)

    def start_library_keyword(self, data, implementation, result):
        self.logger.keyword_start(data, implementation, result)

    def end_library_keyword(self, data, implementation, result):
        self.logger.keyword_end(data, implementation, result)

    def create_dir(self, dir):
        if (path.exists(dir)):
            shutil.rmtree(dir)
        mkdir(dir)

    def dump_to_json(self, file, payload):
        with open(file, 'w') as json_file:
            json.dump(payload, json_file, indent=4)