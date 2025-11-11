import unittest
from vm_translator.src.vm_translator_class import VMTranslator
from vm_translator.src.command import Command
from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemorySegment


class TestVMTranslatorUnit(unittest.TestCase):
    """Unit tests for individual VMTranslator methods"""

    def setUp(self):
        """Create a translator instance for each test"""
        self.translator = VMTranslator(file_name="TestFile")

    def test_translate_add_command(self):
        """Test translation of add command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
        result = self.translator._translate_command(command)
        
        self.assertIn("@SP", result)
        self.assertIn("M=D+M", result)
        self.assertEqual(len(result), 7)

    def test_translate_sub_command(self):
        """Test translation of sub command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.SUB)
        result = self.translator._translate_command(command)
        
        self.assertIn("@SP", result)
        self.assertIn("M=M-D", result)
        self.assertEqual(len(result), 7)

    def test_translate_neg_command(self):
        """Test translation of neg command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.NEG)
        result = self.translator._translate_command(command)
        
        self.assertIn("M=-M", result)

    def test_translate_not_command(self):
        """Test translation of not command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.NOT)
        result = self.translator._translate_command(command)
        
        self.assertIn("M=!M", result)

    def test_translate_and_command(self):
        """Test translation of and command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.AND)
        result = self.translator._translate_command(command)
        
        self.assertIn("M=D&M", result)

    def test_translate_or_command(self):
        """Test translation of or command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.OR)
        result = self.translator._translate_command(command)
        
        self.assertIn("M=D|M", result)

    def test_translate_eq_command(self):
        """Test translation of eq command with unique labels"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.EQ)
        initial_counter = self.translator.label_counter
        result = self.translator._translate_command(command)
        
        # Check that label counter was incremented
        self.assertEqual(self.translator.label_counter, initial_counter + 1)
        # Check for unique labels
        self.assertIn(f"(EQ_TRUE_{initial_counter + 1})", result)
        self.assertIn(f"(END_{initial_counter + 1})", result)
        self.assertIn("D;JEQ", result)

    def test_translate_lt_command(self):
        """Test translation of lt command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.LT)
        result = self.translator._translate_command(command)
        
        self.assertIn("D;JLT", result)

    def test_translate_gt_command(self):
        """Test translation of gt command"""
        command = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.GT)
        result = self.translator._translate_command(command)
        
        self.assertIn("D;JGT", result)

    def test_translate_push_constant(self):
        """Test translation of push constant"""
        command = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
        result = self.translator._translate_command(command)
        
        self.assertIn("@7", result)
        self.assertIn("D=A", result)
        self.assertIn("@SP", result)
        self.assertIn("M=M+1", result)

    def test_translate_push_local(self):
        """Test translation of push local"""
        command = Command(CommandType.PUSH, MemorySegment.LCL, 0)
        result = self.translator._translate_command(command)
        
        self.assertIn("@LCL", result)
        self.assertIn("D=M", result)

    def test_translate_push_argument(self):
        """Test translation of push argument"""
        command = Command(CommandType.PUSH, MemorySegment.ARG, 2)
        result = self.translator._translate_command(command)
        
        self.assertIn("@ARG", result)
        self.assertIn("@2", result)

    def test_translate_push_this(self):
        """Test translation of push this"""
        command = Command(CommandType.PUSH, MemorySegment.THIS, 6)
        result = self.translator._translate_command(command)
        
        self.assertIn("@THIS", result)

    def test_translate_push_that(self):
        """Test translation of push that"""
        command = Command(CommandType.PUSH, MemorySegment.THAT, 5)
        result = self.translator._translate_command(command)
        
        self.assertIn("@THAT", result)

    def test_translate_push_temp(self):
        """Test translation of push temp"""
        command = Command(CommandType.PUSH, MemorySegment.TEMP, 6)
        result = self.translator._translate_command(command)
        
        self.assertIn("@5", result)
        self.assertIn("D=A", result)

    def test_translate_push_static(self):
        """Test translation of push static with filename"""
        command = Command(CommandType.PUSH, MemorySegment.STATIC, 3)
        result = self.translator._translate_command(command)
        
        self.assertIn("@TestFile.3", result)

    def test_translate_push_pointer_0(self):
        """Test translation of push pointer 0 (THIS)"""
        command = Command(CommandType.PUSH, MemorySegment.POINTER, 0)
        result = self.translator._translate_command(command)
        
        self.assertIn("@THIS", result)

    def test_translate_push_pointer_1(self):
        """Test translation of push pointer 1 (THAT)"""
        command = Command(CommandType.PUSH, MemorySegment.POINTER, 1)
        result = self.translator._translate_command(command)
        
        self.assertIn("@THAT", result)

    def test_translate_pop_local(self):
        """Test translation of pop local"""
        command = Command(CommandType.POP, MemorySegment.LCL, 0)
        result = self.translator._translate_command(command)
        
        self.assertIn("@LCL", result)
        self.assertIn("D=M", result)

    def test_translate_pop_argument(self):
        """Test translation of pop argument"""
        command = Command(CommandType.POP, MemorySegment.ARG, 2)
        result = self.translator._translate_command(command)
        
        self.assertIn("@ARG", result)

    def test_translate_pop_temp(self):
        """Test translation of pop temp"""
        command = Command(CommandType.POP, MemorySegment.TEMP, 6)
        result = self.translator._translate_command(command)
        
        self.assertIn("@5", result)

    def test_translate_pop_static(self):
        """Test translation of pop static with filename"""
        command = Command(CommandType.POP, MemorySegment.STATIC, 3)
        result = self.translator._translate_command(command)
        
        self.assertIn("@TestFile.3", result)

    def test_translate_pop_pointer_0(self):
        """Test translation of pop pointer 0 (THIS)"""
        command = Command(CommandType.POP, MemorySegment.POINTER, 0)
        result = self.translator._translate_command(command)
        
        self.assertIn("@THIS", result)

    def test_translate_pop_pointer_1(self):
        """Test translation of pop pointer 1 (THAT)"""
        command = Command(CommandType.POP, MemorySegment.POINTER, 1)
        result = self.translator._translate_command(command)
        
        self.assertIn("@THAT", result)

    def test_translate_with_comments(self):
        """Test that translate adds comments"""
        commands = [
            Command(CommandType.PUSH, MemorySegment.CONSTANT, 7),
            Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
        ]
        result = self.translator.translate(commands, write_comment=True)
        
        # Check comments are present
        self.assertIn("// push constant 7", result)
        self.assertIn("// add", result)

    def test_translate_without_comments(self):
        """Test that translate can omit comments"""
        commands = [
            Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
        ]
        result = self.translator.translate(commands, write_comment=False)
        
        # Check no comments are present
        self.assertNotIn("//", ' '.join(result))

    def test_label_counter_increments(self):
        """Test that label counter increments for each comparison command"""
        commands = [
            Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.EQ),
            Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.LT),
            Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.GT)
        ]
        
        self.assertEqual(self.translator.label_counter, 0)
        self.translator.translate(commands)
        self.assertEqual(self.translator.label_counter, 3)

    def test_static_uses_filename(self):
        """Test that static variables use the correct filename"""
        translator1 = VMTranslator(file_name="File1")
        translator2 = VMTranslator(file_name="File2")
        
        command = Command(CommandType.PUSH, MemorySegment.STATIC, 5)
        
        result1 = translator1._translate_command(command)
        result2 = translator2._translate_command(command)
        
        self.assertIn("@File1.5", result1)
        self.assertIn("@File2.5", result2)


if __name__ == '__main__':
    unittest.main()
