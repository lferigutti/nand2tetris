from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from jack_compiler.syntax_analyzer.xml_writer import XmlWriter


class TestXmlWriter(unittest.TestCase):
    def test_render_returns_empty_string_when_no_content(self):
        writer = XmlWriter()

        self.assertEqual(writer.render(), "")

    def test_render_nested_tags_and_leaf_values(self):
        writer = XmlWriter()

        writer.open_tag("class")
        writer.leaf("keyword", "class")
        writer.leaf("identifier", "Main")
        writer.close_tag("class")

        self.assertEqual(
            writer.render(),
            "<class>\n"
            "  <keyword> class </keyword>\n"
            "  <identifier> Main </identifier>\n"
            "</class>\n",
        )

    def test_leaf_escapes_xml_reserved_characters(self):
        writer = XmlWriter()

        writer.leaf("symbol", "<&>")

        self.assertEqual(writer.render(), "<symbol> &lt;&amp;&gt; </symbol>\n")

    def test_close_tag_raises_when_no_tags_are_open(self):
        writer = XmlWriter()

        with self.assertRaises(ValueError):
            writer.close_tag("class")

    def test_close_tag_raises_for_mismatched_tag(self):
        writer = XmlWriter()
        writer.open_tag("class")

        with self.assertRaises(ValueError):
            writer.close_tag("subroutineDec")

    def test_render_raises_when_tags_are_unclosed(self):
        writer = XmlWriter()
        writer.open_tag("class")

        with self.assertRaises(ValueError):
            writer.render()

    def test_empty_tag_name_raises(self):
        writer = XmlWriter()

        with self.assertRaises(ValueError):
            writer.open_tag("")

        with self.assertRaises(ValueError):
            writer.close_tag("")

        with self.assertRaises(ValueError):
            writer.leaf("", "value")

    def test_write_to_persists_rendered_xml(self):
        writer = XmlWriter()
        writer.open_tag("class")
        writer.close_tag("class")

        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "Main.xml"

            writer.write_to(output_path)

            self.assertEqual(output_path.read_text(), "<class>\n</class>\n")


if __name__ == "__main__":
    unittest.main()