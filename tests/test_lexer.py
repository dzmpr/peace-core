import unittest
from typing import List
from lexer import lexer
from lexer.lexer import Token, TokenClass


def are_tokens_equal(a: Token, b: Token):
    # Check for None both tokens
    if a is b:
        return True
    else:
        # Check for None each of tokens
        if a is None or b is None:
            return False
        # Check tokens
        if a.token_class == b.token_class:
            if a.value == b.value:
                return True
    return False


class TestLexer(unittest.TestCase):
    def is_token_correct(self, input_text: str, expected_output: List[Token]):
        res = lexer.process_line(input_text)
        self.assertEqual(len(res), len(expected_output),
                         f"Result has {len(res)} len when expected len is {len(expected_output)}.")
        for i in range(len(res)):
            self.assertTrue(are_tokens_equal(res[i], expected_output[i]), True)

    def test_word(self):
        input_text = "word"
        result = [Token(TokenClass.word, "word")]
        self.is_token_correct(input_text, result)

    def test_number(self):
        input_text = "100"
        result = [Token(TokenClass.num, "100")]
        self.is_token_correct(input_text, result)

    def test_space(self):
        input_text = " "
        result = [Token(TokenClass.space, " ")]
        self.is_token_correct(input_text, result)

    def test_tab(self):
        input_text = "\t"
        result = [Token(TokenClass.space, "\t")]
        self.is_token_correct(input_text, result)

    def test_undefined(self):
        input_text = "!"
        result = [Token(TokenClass.undefined, "!")]
        self.is_token_correct(input_text, result)

    def test_newline(self):
        input_text = "\n"
        result = [Token(TokenClass.newline, "\n")]
        self.is_token_correct(input_text, result)

    def test_parameter(self):
        input_text = "@"
        result = [Token(TokenClass.parameter, "@")]
        self.is_token_correct(input_text, result)

        input_text = "@10"
        result = [Token(TokenClass.parameter, "@10")]
        self.is_token_correct(input_text, result)

    def test_string(self):
        input_text = "\"string\""
        result = [Token(TokenClass.string, "\"string\"")]
        self.is_token_correct(input_text, result)

    def test_sign(self):
        input_text = "+-/*=#$:,.[]{}()"
        result = [
            Token(TokenClass.sign, "+"),
            Token(TokenClass.sign, "-"),
            Token(TokenClass.sign, "/"),
            Token(TokenClass.sign, "*"),
            Token(TokenClass.sign, "="),
            Token(TokenClass.sign, "#"),
            Token(TokenClass.sign, "$"),
            Token(TokenClass.sign, ":"),
            Token(TokenClass.sign, ","),
            Token(TokenClass.sign, "."),
            Token(TokenClass.sign, "["),
            Token(TokenClass.sign, "]"),
            Token(TokenClass.sign, "{"),
            Token(TokenClass.sign, "}"),
            Token(TokenClass.sign, "("),
            Token(TokenClass.sign, ")")
        ]
        self.is_token_correct(input_text, result)

    def test_all_tokens(self):
        input_text = "Word 123 ! @ \"str\"\nwrd"
        result = [
            Token(TokenClass.word, "Word"),
            Token(TokenClass.space, " "),
            Token(TokenClass.num, "123"),
            Token(TokenClass.space, " "),
            Token(TokenClass.undefined, "!"),
            Token(TokenClass.space, " "),
            Token(TokenClass.parameter, "@"),
            Token(TokenClass.space, " "),
            Token(TokenClass.string, "\"str\""),
            Token(TokenClass.newline, "\n"),
            Token(TokenClass.word, "wrd")
        ]
        self.is_token_correct(input_text, result)


if __name__ == '__main__':
    unittest.main()
