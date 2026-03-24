from itertools import zip_longest
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from jack_compiler.syntax_analyzer.jack_analyzer import JackAnalyser


class TestJackAnalyserIntegration(unittest.TestCase):
    def test_analyze_only_tokens_matches_all_token_fixtures(self):
        fixtures_root = Path(__file__).parent / "test_files"
        for expected_output_path in sorted(fixtures_root.glob("**/*T.xml")):
            input_path = expected_output_path.with_name(
                expected_output_path.name.replace("T.xml", ".jack")
            )

            with self.subTest(fixture=str(expected_output_path.relative_to(fixtures_root))):
                analyzer = JackAnalyser(input_path)
                actual_output = analyzer._analyze(input_path.read_text(), only_tokens=True)
                expected_output = expected_output_path.read_text()

                self._assert_xml_output_matches(
                    actual_output=actual_output,
                    expected_output=expected_output,
                    fixture_path=expected_output_path.relative_to(fixtures_root),
                )

    def _assert_xml_output_matches(
        self,
        actual_output: str,
        expected_output: str,
        fixture_path: Path,
    ) -> None:
        if actual_output == expected_output:
            return

        actual_lines = actual_output.splitlines()
        expected_lines = expected_output.splitlines()

        for line_number, (actual_line, expected_line) in enumerate(
            zip_longest(actual_lines, expected_lines),
            start=1,
        ):
            if actual_line != expected_line:
                self.maxDiff = None
                self.fail(
                    f"Token XML mismatch for {fixture_path} at line {line_number}.\n"
                    f"Expected: {expected_line!r}\n"
                    f"Actual:   {actual_line!r}"
                )

        self.fail(f"Token XML mismatch for {fixture_path}.")


class TestJackAnalyserOutput(unittest.TestCase):
    def test_write_xml_output_writes_token_xml_with_t_suffix(self):
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "Main.jack"
            input_path.write_text("class Main {}")

            output_path = JackAnalyser._write_xml_output(
                input_file_path=input_path,
                xml_output="<tokens>\n</tokens>\n",
                only_tokens=True,
            )

            self.assertEqual(output_path, input_path.with_name("MainT.xml"))
            self.assertEqual(output_path.read_text(), "<tokens>\n</tokens>\n")


if __name__ == "__main__":
    unittest.main()