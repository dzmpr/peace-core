from module_test import ModuleTest

import test_phrase_builder
import test_parse_tree
import test_lang_dict
import test_state_machine
import test_lexer

test_chain = [
    test_state_machine,
    test_lexer,
    test_lang_dict,
    test_phrase_builder,
    test_parse_tree
]
tests = ModuleTest(verbosity=0, verbose_result=True)
tests.test_chain(test_chain)
