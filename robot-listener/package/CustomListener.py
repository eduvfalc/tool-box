from os import path, mkdir, rmdir
import shutil
import json

class CustomListener:
    ROBOT_LISTENER_API_VERSION = 3

    def start_suite(self, data, result):
        self.suite_name = data.name
        self.suite_dir = path.join(path.dirname(__file__), "../output/" + self.suite_name)
        if (path.exists(self.suite_dir)):
            shutil.rmtree(self.suite_dir)
        mkdir(self.suite_dir)

    def start_test(self, data, result):
        self.test_name = data.name 
        self.test_dir = path.join(path.dirname(__file__), "../output/" + self.suite_name + "/" + self.test_name)
        if (path.exists(self.test_dir)):
            rmdir(self.test_dir)
        mkdir(self.test_dir)
    
    def end_suite(self, data, result):
        with open(self.suite_dir + "/" + self.suite_name, 'w') as json_file:
            json.dump(result.to_dict(), json_file, indent=4)

    def end_test(self, data, result):
        with open(self.test_dir + "/" + self.test_name, 'w') as json_file:
            json.dump(result.to_dict(), json_file, indent=4)