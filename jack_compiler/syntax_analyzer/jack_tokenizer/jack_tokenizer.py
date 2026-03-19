from typing import Optional, Union
from jack_compiler.syntax_analyzer.jack_tokenizer.enums import Symbol, TokenType, Keyword

TokenValue = Union[Keyword, Symbol, str, int]


class Token:
    def __init__(
        self,
        value: Optional[TokenValue],
        token_type: TokenType
    ):
        self.value = value
        self.token_type = token_type


class JackTokenizer:

    def __init__(self, file: str):
        """
        Tokenizer for Jack source code

        Here the file is expected to be the content of a .jack file, not the file path. We want the file as 
        a string to simplify the code and do it more directly. 
        The tokenizer will process the content and produce tokens for the syntax analyzer to consume.
        
        """
        self.source = file
        self.current_token: Optional[Token] = None
        self._pos = 0  # Position in the source string
        self._last_pos = len(self.source) - 1

    @property
    def has_more_tokens(self) -> bool:
        return True

    def advance(self) -> None:
        """Get the next token available, it wont retunr it but it will move the cursor to the next token"""
        pass

    def token_type(self) -> TokenType:
        return TokenType.KEYWORD

    def keyword(self) -> Keyword:
        return Keyword.CLASS

    def symbol(self) -> Symbol:
        return Symbol.LEFT_PAREN

    def identifier(self) -> str:
        return ""

    def int_val(self) -> int:
        return 1

    def string_val(self) -> str:
        return ""

    @property
    def _has_next_char(self) -> bool:
        return self._pos < self._last_pos

    @property
    def _current_char(self) -> str:
        return self.source[self._pos]

    @property
    def _next_char(self):
        return self.source[self._pos + 1] if self._has_next_char else None

    def _advance_position(self, amount=1):
        if self._pos + amount <= self._last_pos:
            self._pos += amount
        else:
            raise ValueError("Cannot advance position beyond the end of the source string.")

    def _move_to_next_valid_position(self):

        while self._has_next_char:
            if self._current_char == "/" and self._next_char == "/":
                while self._has_next_char:
                    if self._current_char == '\n':
                        break
                    self._advance_position()

            elif self._current_char == "/" and self._next_char == "*":
                while self._has_next_char:
                    if self._current_char == "*" and self._next_char == "/":
                        self._advance_position()  # Move past the '*'
                        self._advance_position() if self._has_next_char else None  # Move past the '/' if possible
                        break
                    self._advance_position()

            elif self._current_char == '\n':
                self._advance_position()

            elif self._current_char in [' ', '\t', '\r']:
                self._advance_position()
            # We are in a valid position
            else:
                break
