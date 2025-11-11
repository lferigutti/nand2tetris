import unittest
import tempfile
from pathlib import Path
from vm_translator.src.vm_parser import Parser
from vm_translator.src.command import Command
from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemorySegment, BranchingCommand


class TestParser(unittest.TestCase):
  """Test cases for the Parser class"""

  def setUp(self):
    """Create a temporary directory for test files"""
    self.temp_dir = tempfile.mkdtemp()

  def _create_test_file(self, content: str) -> Path:
    """Helper to create a temporary .vm file with given content"""
    file_path = Path(self.temp_dir) / "test.vm"
    with open(file_path, 'w') as f:
      f.write(content)
    return file_path

  def test_parse_arithmetic_command(self):
    """Test parsing a single arithmetic command"""
    file_path = self._create_test_file("add\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.ARITHMETIC)
    self.assertEqual(commands[0].arg1, ArithmeticCommandTypes.ADD)

  def test_parse_push_command(self):
    """Test parsing a push command"""
    file_path = self._create_test_file("push constant 7\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.PUSH)
    self.assertEqual(commands[0].arg1, MemorySegment.CONSTANT)
    self.assertEqual(commands[0].arg2, 7)

  def test_parse_pop_command(self):
    """Test parsing a pop command"""
    file_path = self._create_test_file("pop local 0\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.POP)
    self.assertEqual(commands[0].arg1, MemorySegment.LCL)
    self.assertEqual(commands[0].arg2, 0)

  def test_parse_multiple_commands(self):
    """Test parsing multiple commands"""
    content = """push constant 7
                  push constant 8
                  add
                  if-goto END
                  return
                  call mult 2
        """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 6)
    self.assertTrue(commands[0].is_push())
    self.assertTrue(commands[1].is_push())
    self.assertTrue(commands[2].is_arithmetic())
    self.assertTrue(commands[3].is_branching())
    self.assertTrue(commands[4].is_return())
    self.assertTrue(commands[5].is_call())

  def test_ignore_empty_lines(self):
    """Test that empty lines are ignored"""
    content = """push constant 7
    add
    """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 2)

  def test_ignore_comments(self):
    """Test that comment lines are ignored"""
    content = """// This is a comment
      push constant 7
      // Another comment
      add
      """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 2)

  def test_strip_whitespace(self):
    """Test that leading/trailing whitespace is handled"""
    content = """  push constant 7  
      add  
    """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 2)

  def test_invalid_arithmetic_command(self):
    """Test that invalid arithmetic commands raise SyntaxError"""
    file_path = self._create_test_file("invalid\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_invalid_memory_command(self):
    """Test that invalid memory commands raise SyntaxError"""
    file_path = self._create_test_file("invalid constant 7\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_invalid_memory_segment(self):
    """Test that invalid memory segments raise SyntaxError"""
    file_path = self._create_test_file("push invalid 7\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_invalid_branching_comand(self):
    """Test that invalid memory segments raise SyntaxError"""
    file_path = self._create_test_file("goto LABEL 7\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_parse_label_command(self):
    """Test parsing a label command"""
    file_path = self._create_test_file("label LOOP_START\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.BRANCHING)
    self.assertEqual(commands[0].arg1, BranchingCommand.LABEL)
    self.assertEqual(commands[0].arg2, "LOOP_START")

  def test_parse_goto_command(self):
    """Test parsing a goto command"""
    file_path = self._create_test_file("goto END_PROGRAM\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.BRANCHING)
    self.assertEqual(commands[0].arg1, BranchingCommand.GOTO)
    self.assertEqual(commands[0].arg2, "END_PROGRAM")

  def test_parse_if_goto_command(self):
    """Test parsing an if-goto command"""
    file_path = self._create_test_file("if-goto LOOP\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.BRANCHING)
    self.assertEqual(commands[0].arg1, BranchingCommand.IF_GOTO)
    self.assertEqual(commands[0].arg2, "LOOP")

  def test_parse_function_command(self):
    """Test parsing a function command"""
    file_path = self._create_test_file("function SimpleFunction.test 2\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.FUNCTION)
    self.assertEqual(commands[0].arg1, "SimpleFunction.test")
    self.assertEqual(commands[0].arg2, 2)

  def test_parse_call_command(self):
    """Test parsing a call command"""
    file_path = self._create_test_file("call Math.multiply 2\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.CALL)
    self.assertEqual(commands[0].arg1, "Math.multiply")
    self.assertEqual(commands[0].arg2, 2)

  def test_parse_return_command(self):
    """Test parsing a return command"""
    file_path = self._create_test_file("return\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.RETURN)
    self.assertIsNone(commands[0].arg1)
    self.assertIsNone(commands[0].arg2)

  def test_parse_function_with_zero_locals(self):
    """Test parsing function with zero local variables"""
    file_path = self._create_test_file("function Main.main 0\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].arg2, 0)

  def test_parse_call_with_zero_args(self):
    """Test parsing call with zero arguments"""
    file_path = self._create_test_file("call Sys.init 0\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].arg2, 0)

  def test_parse_mixed_commands_with_branching(self):
    """Test parsing a mix of commands including branching"""
    content = """push constant 0
label LOOP_START
push local 0
push constant 1
add
pop local 0
push local 0
push constant 10
gt
if-goto LOOP_START
"""
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 10)  # Fixed count
    self.assertTrue(commands[0].is_push())
    self.assertTrue(commands[1].is_branching())
    self.assertTrue(commands[9].is_branching())

  def test_parse_function_with_calls_and_return(self):
    """Test parsing function definition with calls and return"""
    content = """function Math.multiply 2
push constant 0
pop local 0
label LOOP
push argument 1
push constant 0
eq
if-goto END
call Math.add 2
return
label END
return
"""
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 12)  # Fixed count
    self.assertTrue(commands[0].is_function())
    self.assertTrue(commands[8].is_call())
    self.assertTrue(commands[9].is_return())
    self.assertTrue(commands[11].is_return())

  def test_parse_all_branching_types(self):
    """Test parsing all branching command types"""
    content = """label START
goto END
if-goto LOOP
"""
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 3)
    self.assertEqual(commands[0].arg1, BranchingCommand.LABEL)
    self.assertEqual(commands[1].arg1, BranchingCommand.GOTO)
    self.assertEqual(commands[2].arg1, BranchingCommand.IF_GOTO)

  def test_parse_labels_with_different_naming(self):
    """Test parsing labels with different naming conventions"""
    content = """label LOOP_START
label END_PROGRAM
label loop123
label $MAIN
"""
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 4)
    self.assertEqual(commands[0].arg2, "LOOP_START")
    self.assertEqual(commands[1].arg2, "END_PROGRAM")
    self.assertEqual(commands[2].arg2, "loop123")
    self.assertEqual(commands[3].arg2, "$MAIN")

  def test_parse_function_names_with_dots(self):
    """Test parsing function names with dots (Class.method)"""
    content = """function Main.fibonacci 0
call Main.fibonacci 1
function Sys.init 0
"""
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 3)
    self.assertEqual(commands[0].arg1, "Main.fibonacci")
    self.assertEqual(commands[1].arg1, "Main.fibonacci")
    self.assertEqual(commands[2].arg1, "Sys.init")

  def test_parse_with_comments_between_branching(self):
    """Test parsing with comments between branching commands"""
    content = """// Start of loop
label LOOP
// Conditional check
if-goto END
// Jump back
goto LOOP
// End label
label END
"""
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 4)

  def test_invalid_function_missing_arg(self):
    """Test that function with missing argument raises SyntaxError"""
    file_path = self._create_test_file("function Foo.bar\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_invalid_call_missing_arg(self):
    """Test that call with missing argument raises SyntaxError"""
    file_path = self._create_test_file("call Foo.bar\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()


if __name__ == '__main__':
  unittest.main()
