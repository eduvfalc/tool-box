from os import path, mkdir, rmdir
from CustomLogger import CustomLogger
from Constants import *
import shutil
import json

class CustomListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, overwite_keyword_logs:bool = False):
        self.custom_logger = CustomLogger(overwite_keyword_logs)

    def start_suite(self, data, result):
        # create suite dir
        self.suite_name = data.name
        self.suite_dir = path.join(path.dirname(__file__), "../output/" + self.suite_name)
        self.create_dir(self.suite_dir)
        self.custom_logger.suite_start(data, result)

    def start_test(self, data, result):
        # create test dir
        self.test_dir = path.join(path.dirname(__file__), "../output/" + self.suite_name + "/" + data.name)
        self.create_dir(self.test_dir)
        self.custom_logger.test_start(data, result)
    
    def end_suite(self, data, result):
        # dump suite results
        self.dump_to_json(self.suite_dir + "/" + data.name, result.to_dict())
        self.custom_logger.suite_end(data, result)

    def end_test(self, data, result):
        # dump test results
        self.dump_to_json(self.test_dir + "/" + data.name, result.to_dict())
        self.custom_logger.test_end(data, result)

    def start_user_keyword(self, data, implementation, result):
        self.custom_logger.user_keyword_start(data, implementation, result)

    def end_user_keyword(self, data, implementation, result):
        self.custom_logger.user_keyword_end(data, implementation, result)

    def create_dir(self, dir):
        if (path.exists(dir)):
            shutil.rmtree(dir)
        mkdir(dir)

    def dump_to_json(self, file, payload):
        with open(file, 'w') as json_file:
            json.dump(payload, json_file, indent=4)