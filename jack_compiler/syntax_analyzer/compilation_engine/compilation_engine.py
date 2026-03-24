from enum import Enum
from typing import Union

from jack_compiler.syntax_analyzer.jack_tokenizer.enums import TokenType, Symbol
from jack_compiler.syntax_analyzer.xml_writer import XmlWriter
from jack_compiler.syntax_analyzer.jack_tokenizer.jack_tokenizer import (
    JackTokenizer,
)


class CompilationEngine:
    def __init__(self, input_file_source: str) -> None:
        self._tokenizer = JackTokenizer(input_file_source)
        self._xml_writer = XmlWriter()

    def compile_class(self) -> str:
        """Compiles a complete class."""
        self._xml_writer.open_tag("class")
        self._advance_and_write_token(TokenType.KEYWORD, "class")
        self._advance_and_write_token(TokenType.IDENTIFIER)
        self._advance_and_write_token(TokenType.SYMBOL, Symbol.LEFT_BRACE)
        self._compile_class_var_dec()
        self._compile_subroutine()
        self._advance_and_write_token(TokenType.SYMBOL, Symbol.RIGHT_BRACE)
        self._xml_writer.close_tag("class")
        return self._xml_writer.render()

    def _compile_class_var_dec(self)-> None:
        pass

    def _compile_subroutine(self) -> None:
        pass

    def _compile_parameter_list(self) -> None:
        pass

    def _compile_subroutine_body(self) -> None:
        pass

    def _compile_var_dec(self) -> None:
        pass

    def _compile_statements(self) -> None:
        pass

    def _compile_let(self) -> None:
        pass

    def _compile_if(self) -> None:
        pass

    def _compile_while(self) -> None:
        pass

    def _compile_do(self) -> None:
        pass

    def _compile_return(self) -> None:
        pass

    def _compile_expression(self) -> None:
        pass

    def _compile_term(self) -> None:
        pass

    def _compile_expression_list(self) -> None:
        pass

    def _advance_and_write_token(self, expected_type: TokenType, expected_token=None):
        if not self._tokenizer.has_more_tokens:
            raise SyntaxError(
                f"Expected token of type {expected_type} with value '{expected_token}', but no more tokens are available"
            )
        self._tokenizer.advance()
        token_type = self._tokenizer.token_type
        normalized_token_value = self._tokenizer.normalized_token_value
        normalized_expected_token = self._normalize_token_value(expected_token)

        if expected_type is not None and expected_type != token_type:
            raise SyntaxError(f"Expected token type {expected_type}, but got {token_type}")

        if expected_token is not None and normalized_token_value != normalized_expected_token:
            raise SyntaxError(
                f"Expected token '{normalized_expected_token}', but got '{normalized_token_value}'"
            )

        self._xml_writer.leaf(self._tokenizer.token_type.value, str(normalized_token_value))
    
    @staticmethod
    def _normalize_token_value(value) -> Union[str, int, None]:
        if isinstance(value, Enum):
            return value.value
        return value