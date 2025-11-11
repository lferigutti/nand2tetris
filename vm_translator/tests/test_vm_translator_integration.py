import unittest
from pathlib import Path
from vm_translator.src.vm_parser import Parser
from vm_translator.src.vm_translator_class import VMTranslator


class TestVMTranslatorIntegration(unittest.TestCase):
    """Integration tests using actual nand2tetris test files"""

    def setUp(self):
        """Set up paths to test files"""
        self.test_dir = Path(__file__).parent / "test_files"

    def _parse_and_translate(self, vm_file: str) -> list[str]:
        """Helper to parse a VM file and translate it"""
        vm_path = self.test_dir / vm_file
        file_name = vm_path.stem  # Get filename without extension
        
        parser = Parser(vm_path)
        commands = parser.parse()
        
        translator = VMTranslator(file_name=file_name)
        return translator.translate(commands, write_comment=True)

    def _read_expected_asm(self, asm_file: str) -> list[str]:
        """Helper to read expected assembly output"""
        asm_path = self.test_dir / asm_file
        with open(asm_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def test_simple_add_integration(self):
        """Test SimpleAdd.vm produces correct assembly"""
        result = self._parse_and_translate("SimpleAdd.vm")
        expected = self._read_expected_asm("SimpleAdd.asm")
        
        # Remove comments for comparison
        result_no_comments = [line for line in result if not line.startswith("//")]
        expected_no_comments = [line for line in expected if not line.startswith("//")]
        
        self.assertEqual(result_no_comments, expected_no_comments)

    def test_stack_test_integration(self):
        """Test StackTest.vm produces correct assembly"""
        result = self._parse_and_translate("StackTest.vm")
        expected = self._read_expected_asm("StackTest.asm")
        
        result_no_comments = [line for line in result if not line.startswith("//")]
        expected_no_comments = [line for line in expected if not line.startswith("//")]
        
        self.assertEqual(result_no_comments, expected_no_comments)

    def test_basic_test_integration(self):
        """Test BasicTest.vm produces correct assembly"""
        result = self._parse_and_translate("BasicTest.vm")
        expected = self._read_expected_asm("BasicTest.asm")
        
        result_no_comments = [line for line in result if not line.startswith("//")]
        expected_no_comments = [line for line in expected if not line.startswith("//")]
        
        self.assertEqual(result_no_comments, expected_no_comments)

    def test_pointer_test_integration(self):
        """Test PointerTest.vm produces correct assembly"""
        result = self._parse_and_translate("PointerTest.vm")
        expected = self._read_expected_asm("PointerTest.asm")
        
        result_no_comments = [line for line in result if not line.startswith("//")]
        expected_no_comments = [line for line in expected if not line.startswith("//")]
        
        self.assertEqual(result_no_comments, expected_no_comments)

    def test_static_test_integration(self):
        """Test StaticTest.vm produces correct assembly"""
        result = self._parse_and_translate("StaticTest.vm")
        expected = self._read_expected_asm("StaticTest.asm")
        
        result_no_comments = [line for line in result if not line.startswith("//")]
        expected_no_comments = [line for line in expected if not line.startswith("//")]
        
        self.assertEqual(result_no_comments, expected_no_comments)

    def test_simple_push_pop_integration(self):
        """Test SimplePushPop.vm produces correct assembly"""
        result = self._parse_and_translate("SimplePushPop.vm")
        expected = self._read_expected_asm("SimplePushPop.asm")
        
        result_no_comments = [line for line in result if not line.startswith("//")]
        expected_no_comments = [line for line in expected if not line.startswith("//")]
        
        self.assertEqual(result_no_comments, expected_no_comments)

    def test_simple_add_command_count(self):
        """Test that SimpleAdd produces the expected number of commands"""
        result = self._parse_and_translate("SimpleAdd.vm")
        
        # SimpleAdd has: push constant 7, push constant 8, add
        # Should have 3 comments
        comments = [line for line in result if line.startswith("//")]
        self.assertEqual(len(comments), 3)

    def test_all_files_parse_successfully(self):
        """Test that all VM files can be parsed and translated without errors"""
        vm_files = [
            "SimpleAdd.vm",
            "StackTest.vm",
            "BasicTest.vm",
            "PointerTest.vm",
            "StaticTest.vm",
            "SimplePushPop.vm"
        ]
        
        for vm_file in vm_files:
            with self.subTest(file=vm_file):
                try:
                    result = self._parse_and_translate(vm_file)
                    self.assertIsInstance(result, list)
                    self.assertGreater(len(result), 0)
                except Exception as e:
                    self.fail(f"Failed to parse and translate {vm_file}: {e}")

    def test_static_variable_uses_filename(self):
        """Test that static variables use the correct filename prefix"""
        result = self._parse_and_translate("StaticTest.vm")
        
        # StaticTest should have @StaticTest.X references
        asm_code = '\n'.join(result)
        self.assertIn("@StaticTest.", asm_code)

    def test_comparison_labels_are_unique(self):
        """Test that comparison commands generate unique labels"""
        result = self._parse_and_translate("StackTest.vm")
        
        # Collect all labels
        labels = [line for line in result if line.startswith("(")]
        
        # Check that labels are unique
        self.assertEqual(len(labels), len(set(labels)))


if __name__ == '__main__':
    unittest.main()
