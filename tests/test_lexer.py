import unittest
from lexer import lexer
from lexer.lexer import Token, TokenClass


def are_tokens_equal(a: Token, b: Token):
    if a.token_class == b.token_class:
        if a.value == b.value:
            return True
    return False


class TestLexer(unittest.TestCase):
    def test_word(self):
        res = lexer.process_line("word\n")
        exp = [Token(TokenClass.word, "word"), Token(TokenClass.newline, "\n")]
        self.assertEqual(len(res), len(exp))
        for i in range(len(res)):
            with self.subTest(i=i):
                self.assertTrue(are_tokens_equal(res[i], exp[i]), True)

    def test_all_tokens(self):
        res = lexer.process_line("Word 123 ! @ \"string\"\n")
        exp = [
            Token(TokenClass.word, "Word"),
            Token(TokenClass.space, " "),
            Token(TokenClass.num, "123"),
            Token(TokenClass.space, " "),
            Token(TokenClass.undefined, "!"),
            Token(TokenClass.space, " "),
            Token(TokenClass.parameter, "@"),
            Token(TokenClass.space, " "),
            Token(TokenClass.string, "\"string\""),
            Token(TokenClass.newline, "\n")
        ]
        self.assertEqual(len(res), len(exp), f"Result:\n{res}\nExpected:\n{exp}")
        for i in range(len(exp)):
            with self.subTest(i=i):
                self.assertTrue(are_tokens_equal(res[i], exp[i]),
                                msg=f"\nExpected - {str(exp[i])}\nResult - {str(res[i])}")


if __name__ == '__main__':
    unittest.main()
