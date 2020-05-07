from typing import Union
from unittest import TestResult, TestLoader, TextTestRunner


class ModuleTest:
    def __init__(self, verbosity: int = 1, verbose_result: bool = False):
        self.test_loader = TestLoader()
        self.test_suite = None
        self.runner = TextTestRunner(verbosity=verbosity)
        self.test_result: Union[TestResult, None] = None
        self.verbose_result = verbose_result

    def print_result(self, name: str):
        print(f"Tested {name} module.")
        print(f"Errors: {len(self.test_result.errors)}")
        print(f"Failures: {len(self.test_result.failures)}")
        print(f"Skipped: {len(self.test_result.skipped)}")
        print(f"Tested: {self.test_result.testsRun}")

    def test_module(self, module) -> bool:
        self.test_suite = self.test_loader.loadTestsFromModule(module)
        self.test_result = self.runner.run(self.test_suite)
        if self.verbose_result:
            self.print_result(module.__name__)
        if (len(self.test_result.errors) > 0 or
                len(self.test_result.failures) > 0):
            return False
        return True