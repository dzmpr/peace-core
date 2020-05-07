from module_test import ModuleTest

import test_lexer

tests = ModuleTest(verbosity=0, verbose_result=True)
print(tests.test_module(test_lexer))
