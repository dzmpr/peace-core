from module_test import ModuleTest

import test_state_machine
import test_lexer

test_chain = [test_state_machine, test_lexer]
tests = ModuleTest(verbosity=0, verbose_result=True)
tests.test_chain(test_chain)
