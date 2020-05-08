import unittest

from syntaxer.lang_dict import LangDict, SignatureType, Signature
from lexer.token import TokenClass


def are_signatures_equal(signature: Signature, reference: Signature) -> bool:
    if signature.definition != reference.definition:
        return False
    if signature.output != reference.output:
        return False
    if signature.params != reference.params:
        return False
    if signature.required_params != reference.required_params:
        return False
    if signature.max_params != reference.max_params:
        return False
    if signature.contains_param != reference.contains_param:
        return False
    if signature.uses_number != reference.uses_number:
        return False
    if signature.signature_type != reference.signature_type:
        return False
    return True


class TestLangDict(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.language_dictionary = LangDict()
        cls.language_dictionary.add_signature("test", SignatureType.operator, "TEST", 1, [
            TokenClass.string
        ])
        cls.language_dictionary.add_signature("test1", SignatureType.operator, "TEST1", 1, [
            TokenClass.num
        ])
        cls.language_dictionary.add_signature("test2", SignatureType.operator, "TEST2", 1, [
            TokenClass.word
        ])

    def test_get_candidates(self):
        self.assertEqual(1, len(self.language_dictionary.get_candidates("test2")))
        self.assertEqual(0, len(self.language_dictionary.get_candidates("test0")))

    def test_add_signature(self):
        self.assertEqual(1, len(self.language_dictionary.get_candidates("test")))
        self.language_dictionary.add_signature("test", SignatureType.operator, "TEST3", 1, [
            TokenClass.word
        ])
        self.assertEqual(2, len(self.language_dictionary.get_candidates("test")))

    def test_get_signature(self):
        signature = self.language_dictionary.get_signature(self.language_dictionary.get_candidates("test1")[0])
        expected = Signature(SignatureType.operator, "test1", "TEST1", 1, 1, [TokenClass.num])
        self.assertTrue(are_signatures_equal(signature, expected))


if __name__ == '__main__':
    unittest.main()
