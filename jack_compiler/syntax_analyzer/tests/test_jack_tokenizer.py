import unittest

from jack_compiler.syntax_analyzer.jack_tokenizer.enums import Keyword, Symbol, TokenType
from jack_compiler.syntax_analyzer.jack_tokenizer.jack_tokenizer import JackTokenizer, Token


class TestToken(unittest.TestCase):
    def test_token_stores_value_and_type(self):
        token = Token(value=Keyword.CLASS, token_type=TokenType.KEYWORD)

        self.assertEqual(token.value, Keyword.CLASS)
        self.assertEqual(token.token_type, TokenType.KEYWORD)

    def test_token_allows_none_value(self):
        token = Token(value=None, token_type=TokenType.IDENTIFIER)

        self.assertIsNone(token.value)
        self.assertEqual(token.token_type, TokenType.IDENTIFIER)


class TestJackTokenizerLowLevel(unittest.TestCase):
    def test_init_sets_initial_state(self):
        tokenizer = JackTokenizer("class Main {}")

        self.assertEqual(tokenizer.source, "class Main {}")
        self.assertIsNone(tokenizer.current_token)
        self.assertEqual(tokenizer._pos, 0)
        self.assertEqual(tokenizer._last_pos, len("class Main {}") - 1)

    def test_current_char_returns_character_at_current_position(self):
        tokenizer = JackTokenizer("abc")

        self.assertEqual(tokenizer._current_char, "a")

    def test_next_char_returns_following_character(self):
        tokenizer = JackTokenizer("abc")

        self.assertEqual(tokenizer._next_char, "b")

    def test_next_char_returns_none_at_last_position(self):
        tokenizer = JackTokenizer("ab")
        tokenizer._advance_position()

        self.assertIsNone(tokenizer._next_char)

    def test_advance_position_moves_cursor_by_one_by_default(self):
        tokenizer = JackTokenizer("abc")

        tokenizer._advance_position()

        self.assertEqual(tokenizer._pos, 1)

    def test_advance_position_moves_cursor_by_given_amount(self):
        tokenizer = JackTokenizer("abcdef")

        tokenizer._advance_position(3)

        self.assertEqual(tokenizer._pos, 3)

    def test_move_to_next_valid_position_does_not_move_when_already_valid(self):
        tokenizer = JackTokenizer("let x = 1;")

        tokenizer._move_to_next_valid_position()

        self.assertEqual(tokenizer._current_char, "l")

    def test_move_to_next_valid_position_skips_newline(self):
        tokenizer = JackTokenizer("\nlet x = 1;")

        tokenizer._move_to_next_valid_position()

        self.assertEqual(tokenizer._current_char, "l")

    def test_move_to_next_valid_position_skips_line_comment(self):
        tokenizer = JackTokenizer("// comment\nlet x = 1;")

        tokenizer._move_to_next_valid_position()

        self.assertEqual(tokenizer._current_char, "l")

    def test_move_to_next_valid_position_skips_block_comment(self):
        tokenizer = JackTokenizer("/* comment */\nlet x = 1;")

        tokenizer._move_to_next_valid_position()

        self.assertEqual(tokenizer._current_char, "l")

    def test_move_to_next_valid_position_skips_spaces_tabs_and_carriage_return(self):
        tokenizer = JackTokenizer(" \t\rlet x = 1;")

        tokenizer._move_to_next_valid_position()

        self.assertEqual(tokenizer._current_char, "l")

    def test_move_to_next_valid_position_end_with_comment(self):
        tokenizer = JackTokenizer("/* comment */")

        self.assertEqual(tokenizer._current_char, "/")
        tokenizer._move_to_next_valid_position()
        self.assertFalse(tokenizer._has_next_char)

    class TestJackTokenizerAPI(unittest.TestCase):

        def test_has_more_tokens_returns_false_when_no_more_tokens(self):
            tokenizer = JackTokenizer("")
            self.assertTrue(tokenizer.has_more_tokens)


if __name__ == "__main__":
    unittest.main()
