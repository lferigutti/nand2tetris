import unittest

from jack_compiler.syntax_analyzer.compilation_engine.compilation_engine import (
    CompilationEngine,
)


class TestCompilationEngine(unittest.TestCase):
    def test_compile_class_with_empty_main_class(self):
        engine = CompilationEngine("class Main {}")

        self.assertEqual(
            engine.compile_class(),
            "<class>\n"
            "  <keyword> class </keyword>\n"
            "  <identifier> Main </identifier>\n"
            "  <symbol> { </symbol>\n"
            "  <symbol> } </symbol>\n"
            "</class>\n",
        )


if __name__ == "__main__":
    unittest.main()
