import unittest
from test_lexer import are_tokens_equal

from syntaxer.phrase_builder import phrase_builder
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from lexer.token import TokenClass, Token


def are_phrases_equal(phrase: Phrase, reference: Phrase):
    def print_difference(place, a, b):
        print(f"Found difference in {place}.")
        print(f"Resulted \"{str(a)}\" isn't equals to expected \"{str(b)}\".")

    if not are_tokens_equal(phrase.keyword, reference.keyword):
        print_difference("keywords", phrase.keyword, reference.keyword)
        return False
    if phrase.signature_id != reference.signature_id:
        print_difference("signature_id", phrase.signature_id, reference.signature_id)
        return False
    if phrase.phrase_class != reference.phrase_class:
        print_difference("phrase_classes", phrase.phrase_class, reference.phrase_class)
        return False
    if phrase.phrase_subclass != reference.phrase_subclass:
        print_difference("phrase_subclasses", phrase.phrase_subclass, reference.phrase_subclass)
        return False
    # Phrase hasn't parameters
    if phrase.params is reference.params:
        return True
    else:
        # One of phrases hasn't parameters
        if phrase.params is None or reference.params is None:
            print_difference("parameters type", phrase.params, reference.params)
            return False
        # Both have parameters
        else:
            if len(phrase.params) != len(reference.params):
                print_difference("parameters length", len(phrase.params), len(reference.params))
                return False
            for i in range(len(phrase.params)):
                if not are_tokens_equal(phrase.params[i], reference.params[i]):
                    print_difference(f"parameter i={i}", phrase.params[i], reference.params[i])
                    return False
    return True


class TestPhraseBuilder(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.program_context = Phrase(PhraseClass.block, PhraseSubclass.program)
        cls.expression_context = Phrase(PhraseClass.block, PhraseSubclass.expression)
        cls.device_context = Phrase(PhraseClass.block, PhraseSubclass.device)
        cls.body_context = Phrase(PhraseClass.block, PhraseSubclass.body)

    # Test block building
    def test_build_expression(self):
        built_phrase = phrase_builder(self.program_context, PhraseClass.block,
                                      [Token(TokenClass.word, "expression")], 0)
        expected_expr = Phrase(PhraseClass.block, PhraseSubclass.expression,
                               keyword=Token(TokenClass.word, "expression"))
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    def test_build_device_in_expression(self):
        built_phrase = phrase_builder(self.expression_context, PhraseClass.block,
                                      [Token(TokenClass.word, "device_in_expression")], 0)
        expected_expr = Phrase(PhraseClass.block, PhraseSubclass.device,
                               keyword=Token(TokenClass.word, "device_in_expression"))
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    def test_build_device_in_body(self):
        built_phrase = phrase_builder(self.body_context, PhraseClass.block,
                                      [Token(TokenClass.word, "device_in_body")], 0)
        expected_expr = Phrase(PhraseClass.block, PhraseSubclass.device,
                               keyword=Token(TokenClass.word, "device_in_body"))
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    # Test building label
    def test_build_label(self):
        built_phrase = phrase_builder(self.expression_context, PhraseClass.label,
                                      [Token(TokenClass.word, "label")], 0)
        expected_expr = Phrase(PhraseClass.label, phrase_subclass=None,
                               keyword=Token(TokenClass.word, "label"), params=[])
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    def test_build_parametrised_label(self):
        built_phrase = phrase_builder(self.expression_context, PhraseClass.label,
                                      [Token(TokenClass.word, "label"),
                                       Token(TokenClass.parameter, "@")], 0)
        expected_expr = Phrase(PhraseClass.label, phrase_subclass=None,
                               keyword=Token(TokenClass.word, "label"), params=[Token(TokenClass.parameter, "@")])
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    # Test building comment
    def test_build_comment(self):
        built_phrase = phrase_builder(self.body_context, PhraseClass.comment,
                                      [Token(TokenClass.word, "w1"),
                                       Token(TokenClass.word, "w2"),
                                       Token(TokenClass.word, "w3")], 0)
        expected_expr = Phrase(PhraseClass.comment, phrase_subclass=None,
                               params=[Token(TokenClass.word, "w1"),
                                       Token(TokenClass.word, "w2"),
                                       Token(TokenClass.word, "w3")])
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    # Test building block close
    def test_build_block_close(self):
        built_phrase = phrase_builder(self.program_context, PhraseClass.blockClose, [], 0)
        expected_expr = Phrase(PhraseClass.blockClose, phrase_subclass=None,
                               keyword=None, params=None)
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    # Test building operator
    def test_build_empty_operator(self):
        built_phrase = phrase_builder(self.expression_context, PhraseClass.operator, [
            Token(TokenClass.word, "delay")
        ], 0)
        expected_expr = Phrase(PhraseClass.operator, phrase_subclass=None,
                               keyword=Token(TokenClass.word, "delay"), params=[])
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))

    def test_build_operator_with_parameters(self):
        built_phrase = phrase_builder(self.expression_context, PhraseClass.operator, [
            Token(TokenClass.word, "delay"),
            Token(TokenClass.num, "1"),
            Token(TokenClass.word, "two"),
            Token(TokenClass.string, "\"3\""),
            Token(TokenClass.parameter, "@4")
        ], 0)
        expected_expr = Phrase(PhraseClass.operator, phrase_subclass=None,
                               keyword=Token(TokenClass.word, "delay"),
                               params=[Token(TokenClass.num, "1"),
                                       Token(TokenClass.word, "two"),
                                       Token(TokenClass.string, "\"3\""),
                                       Token(TokenClass.parameter, "@4")])
        self.assertTrue(are_phrases_equal(built_phrase, expected_expr))


if __name__ == '__main__':
    unittest.main()
