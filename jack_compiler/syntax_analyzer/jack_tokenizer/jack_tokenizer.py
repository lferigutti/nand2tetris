from typing import Optional, Union, cast
from jack_compiler.syntax_analyzer.jack_tokenizer.enums import Symbol, TokenType, Keyword

TokenValue = Union[Keyword, Symbol, str, int]


class Token:
    def __init__(
        self,
        value: TokenValue,
        token_type: TokenType
    ):
        self.value = value
        self.token_type = token_type

    @property
    def actual_value(self):
        return self.value.value if not isinstance(self.value, (int, str)) else str(self.value)


class JackTokenizer:

    def __init__(self, file: str):
        """
        Tokenizer for Jack source code

        Here the file is expected to be the content of a .jack file, not the file path. We want the file as 
        a string to simplify the code and do it more directly. 
        The tokenizer will process the content and produce tokens for the syntax analyzer to consume.
        
        """
        self._source = file
        self._current_token: Optional[Token] = None
        self._pos = 0  # Position in the source string
        self._last_pos = len(self._source) - 1
        self._has_more_tokens = True

    @property
    def has_more_tokens(self) -> bool:
        current_pos = self._pos
        try:
            if not self._has_current_char:
                return False

            self._move_to_next_valid_position()
            return self._has_current_char
        finally:
            self._pos = current_pos

    def advance(self) -> None:
        """
        Get the next token available, it won't return it, but it will move the cursor to the next token available,
        if there is one. If there are no more tokens, it should do nothing.
        """
        if not self.has_more_tokens:
            return

        self._move_to_next_valid_position()
        self._current_token = self._build_token()

    @property
    def token_type(self) -> TokenType:
        if self._current_token is not None:
            return self._current_token.token_type
        else:
            raise ValueError("There is no current token available")

    def keyword(self) -> Keyword:
        return Keyword(self._return_token_value_or_raise(TokenType.KEYWORD))

    def symbol(self) -> Symbol:
        return Symbol(self._return_token_value_or_raise(TokenType.SYMBOL))

    def identifier(self) -> str:
        return str(self._return_token_value_or_raise(TokenType.IDENTIFIER))

    def int_val(self) -> int:
        return cast(int, self._return_token_value_or_raise(TokenType.INT_CONST))

    def string_val(self) -> str:
        return str(self._return_token_value_or_raise(TokenType.STRING_CONST))

    @property
    def token_value(self) -> TokenValue:
        """ More general method to avoid complicated proposed API """
        if self._current_token is None:
            raise ValueError("There is no current token available")

        return self._current_token.value

    def _return_token_value_or_raise(self, token_type: TokenType) -> TokenValue:
        """ Factory function to avoid duplication"""

        if self._current_token is None:
            raise ValueError("There is not current token")

        if self._current_token.token_type != token_type:
            raise ValueError(f"The current token is not a {token_type.value}")

        return self._current_token.value

    @property
    def _has_next_char(self) -> bool:
        return self._pos < self._last_pos

    @property
    def _has_current_char(self) -> bool:
        return self._pos <= self._last_pos

    @property
    def _current_char(self) -> str:
        return self._source[self._pos]

    @property
    def _next_char(self):
        return self._source[self._pos + 1] if self._has_next_char else None

    def _advance_position(self, amount=1):
        if self._pos + amount <= self._last_pos + 1:
            self._pos += amount
        else:
            raise ValueError("Cannot advance position beyond the end of the source string.")

    def _move_to_next_valid_position(self):
        """
        Move the position to the next valid character, skipping over comments, whitespace, and newlines.
        This method does not return anything, it just moves the position to the next valid character.
        If we are currently in a valid position, it would not move
        """
        while self._has_current_char:
            if self._current_char == "/" and self._next_char == "/":
                while self._has_current_char:
                    if self._current_char == '\n':
                        break
                    self._advance_position()

            elif self._current_char == "/" and self._next_char == "*":
                while self._has_current_char:
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
                return

    def _build_token(self) -> Optional[Token]:
        if self._current_char in Symbol:
            return self._build_symbol()
        elif self._current_char.isdigit():
            return self._build_integer_constant()
        elif self._current_char == '"':
            return self._build_string_constant()
        elif self._current_char.isalpha() or self._current_char == '_':
            return self._build_keyword_or_identifier()
        else:
            raise ValueError(f"Unexpected character '{self._current_char}' at position {self._pos}")

    def _build_symbol(self) -> Token:
        symbol = self._current_char

        self._advance_position()

        return Token(value=Symbol(symbol), token_type=TokenType.SYMBOL)

    def _build_integer_constant(self) -> Token:
        number = ""
        while self._has_current_char and self._current_char.isdigit():
            number += self._current_char
            self._advance_position()

        return Token(value=int(number), token_type=TokenType.INT_CONST)

    def _build_string_constant(self) -> Token:
        string_constant = ""

        if self._has_next_char:
            # Move out of the "
            self._advance_position()
        else:
            raise SyntaxError("There is no next token to build a string constant")

        while self._has_current_char and self._current_char != '"':
            string_constant += self._current_char
            self._advance_position()

        if not self._has_current_char:
            raise SyntaxError("There is no next token to build a string constant")

        self._advance_position()

        return Token(value=str(string_constant), token_type=TokenType.STRING_CONST)

    def _build_keyword_or_identifier(self) -> Token:
        """Assume the first value is not a digit."""
        string_constant = ""

        while self._has_current_char and (self._current_char.isalnum() or self._current_char == "_"):
            string_constant += self._current_char
            self._advance_position()

        if string_constant in Keyword:
            return Token(value=Keyword(string_constant), token_type=TokenType.KEYWORD)
        return Token(value=str(string_constant), token_type=TokenType.IDENTIFIER)
