from pathlib import Path
import sys

from jack_compiler.syntax_analyzer.jack_tokenizer.jack_tokenizer import JackTokenizer
from jack_compiler.syntax_analyzer.xml_writer import XmlWriter
from jack_compiler.syntax_analyzer.compilation_engine.compilation_engine import CompilationEngine


class JackAnalyser:
    def __init__(self, input_path: Path):
        self._jack_files = self._get_jack_files(input_path)

    def run(self, only_tokens: bool = False) -> list[Path]:
        output_paths: list[Path] = []

        for jack_file in self._jack_files:
            source = jack_file.read_text()
            result = self._analyze(source, only_tokens)
            output_paths.append(self._write_xml_output(jack_file, result, only_tokens))

        return output_paths

    @staticmethod
    def _get_jack_files(input_path: Path) -> list[Path]:
        if input_path.is_dir():
            files = list(input_path.glob("*.jack"))
            if not files:
                print(f"Error: no .jack files found in '{input_path}'", file=sys.stderr)
                sys.exit(1)
            return files
        if input_path.suffix != ".jack":
            print(f"Error: '{input_path}' is not a .jack file", file=sys.stderr)
            sys.exit(1)
        return [input_path]

    def _analyze(self, input_file_source: str, only_tokens: bool = False) -> str:
        if only_tokens:
            return self._analyze_only_tokens(input_file_source)
        compilation_engine = CompilationEngine(input_file_source)
        return compilation_engine.compile_class()

    @classmethod
    def _write_xml_output(
        cls,
        input_file_path: Path,
        xml_output: str,
        only_tokens: bool = False,
    ) -> Path:
        output_path = cls._get_output_path(input_file_path, only_tokens)
        output_path.write_text(xml_output)
        return output_path

    @staticmethod
    def _get_output_path(input_file_path: Path, only_tokens: bool = False) -> Path:
        suffix = "T.xml" if only_tokens else ".xml"
        return input_file_path.with_name(f"{input_file_path.stem}{suffix}")

    @staticmethod
    def _analyze_only_tokens(input_file_source: str) -> str:
        """ This methods is for testing purposes only"""
        tokenizer = JackTokenizer(input_file_source)
        wr = XmlWriter(indent="")

        wr.open_tag("tokens")
        while tokenizer.has_more_tokens:
            tokenizer.advance()
            wr.leaf(tokenizer.token_type.value, str(tokenizer.normalized_token_value))
        wr.close_tag("tokens")

        return wr.render()
