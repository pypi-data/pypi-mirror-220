import yaml
import importlib
from collections import deque

class Parserito:
    def __init__(self, tests_module_name, config_file):
        self.tests_module = importlib.import_module(tests_module_name)
        self.config_file = config_file
        self.config = {}
        self.queue = deque()

    def load_config_file(self, yaml_file):
        try:
            with open(yaml_file, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"The file {yaml_file} was not found.")
            return
        
        steps = self.config.get('steps', {})

        for step_name, step_params in steps.items():
            try:
                test_func = getattr(self.tests_module, step_name.replace("-", "_"))
            except AttributeError:
                print(f"The function {step_name} was not found in the tests module.")
                continue
            
            task = (test_func, step_params)
            self.queue.append(task)


    def run(self):
        while self.queue:
            test_func, step_params = self.queue.popleft()

            try:
                test_func(**step_params)
            except Exception as e:
                print(f"An error occurred while running the function {test_func.__name__}: {str(e)}")







        
