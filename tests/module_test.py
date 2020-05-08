from typing import Union
from types import ModuleType
from unittest import TestResult, TestLoader, TextTestRunner


class ModuleTest:
    def __init__(self, verbosity: int = 1, verbose_result: bool = False):
        self._tested_modules: int = 0
        self._total_errors: int = 0
        self._total_failures: int = 0
        self._total_skipped: int = 0
        self._total_tested: int = 0
        self.test_loader = TestLoader()
        self.test_suite = None
        self.runner = TextTestRunner(verbosity=verbosity)
        self.test_result: Union[TestResult, None] = None
        self.verbose_result = verbose_result

    def _record_results(self):
        self._total_errors += len(self.test_result.errors)
        self._total_failures += len(self.test_result.failures)
        self._total_skipped += len(self.test_result.skipped)
        self._total_tested += self.test_result.testsRun

    def print_result(self, name: str):
        print(f"Tested {name} module.")
        print(f"Errors: {len(self.test_result.errors)}.")
        print(f"Failures: {len(self.test_result.failures)}.")
        print(f"Skipped: {len(self.test_result.skipped)}.")
        print(f"Tested: {self.test_result.testsRun}.", end="\n\n")

    def print_total_results(self):
        print(f"Tested {self._tested_modules} modules.")
        print(f"Total errors: {self._total_errors}.")
        print(f"Total failures: {self._total_failures}.")
        print(f"Total skipped: {self._total_skipped}.")
        print(f"Total tested: {self._total_tested}.", end="\n\n")

    def test_module(self, module) -> bool:
        self._tested_modules += 1
        self.test_suite = self.test_loader.loadTestsFromModule(module)
        self.test_result = self.runner.run(self.test_suite)

        if self.verbose_result:
            self.print_result(module.__name__)

        self._record_results()

        if (len(self.test_result.errors) > 0 or
                len(self.test_result.failures) > 0):
            return False
        return True

    def _is_only_modules(self, module_list):
        is_only_modules = True
        for index, module in enumerate(module_list):
            if not isinstance(module, ModuleType):
                is_only_modules = False
                if self.verbose_result:
                    print(f"Found not a module at {index} position.")
        return is_only_modules

    def test_chain(self, module_list):
        if not self._is_only_modules(module_list):
            print("Test aborted.")
            return

        is_no_errors = True
        for module in module_list:
            if is_no_errors:
                is_no_errors = self.test_module(module)
                if not is_no_errors:
                    print(f"Test chain broken in {module.__name__} module.")
            else:
                print(f"Skip testing for module {module.__name__}.")
        if self.verbose_result:
            self.print_total_results()
        return is_no_errors
