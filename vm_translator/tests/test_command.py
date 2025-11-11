import unittest
from vm_translator.src.command import Command
from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemorySegment, BranchingCommand


class TestCommand(unittest.TestCase):
  """Test cases for the Command class"""

  def test_arithmetic_command_creation(self):
    """Test creating an arithmetic command"""
    cmd = Command(
      command_type=CommandType.ARITHMETIC,
      arg1=ArithmeticCommandTypes.ADD
    )
    self.assertEqual(cmd.command_type, CommandType.ARITHMETIC)
    self.assertEqual(cmd.arg1, ArithmeticCommandTypes.ADD)
    self.assertIsNone(cmd.arg2)

  def test_push_command_creation(self):
    """Test creating a push command"""
    cmd = Command(
      command_type=CommandType.PUSH,
      arg1=MemorySegment.CONSTANT,
      arg2=7
    )
    self.assertEqual(cmd.command_type, CommandType.PUSH)
    self.assertEqual(cmd.arg1, MemorySegment.CONSTANT)
    self.assertEqual(cmd.arg2, 7)

  def test_pop_command_creation(self):
    """Test creating a pop command"""
    cmd = Command(
      command_type=CommandType.POP,
      arg1=MemorySegment.LCL,
      arg2=0
    )
    self.assertEqual(cmd.command_type, CommandType.POP)
    self.assertEqual(cmd.arg1, MemorySegment.LCL)
    self.assertEqual(cmd.arg2, 0)

  def test_branching_command_creation(self):
    cmd = Command(
      command_type=CommandType.BRANCHING,
      arg1=BranchingCommand.GOTO,
      arg2="LOOP"
    )
    self.assertEqual(cmd.command_type, CommandType.BRANCHING)
    self.assertEqual(cmd.arg1, BranchingCommand.GOTO)
    self.assertEqual(cmd.arg2, "LOOP")

  def test_function_command_creation(self):
    """Test creating a function command"""
    cmd = Command(
      command_type=CommandType.FUNCTION,
      arg1="SimpleFunction.test",
      arg2=2
    )
    self.assertEqual(cmd.command_type, CommandType.FUNCTION)
    self.assertEqual(cmd.arg1, "SimpleFunction.test")
    self.assertEqual(cmd.arg2, 2)

  def test_call_command_creation(self):
    """Test creating a call command"""
    cmd = Command(
      command_type=CommandType.CALL,
      arg1="Math.multiply",
      arg2=2
    )
    self.assertEqual(cmd.command_type, CommandType.CALL)
    self.assertEqual(cmd.arg1, "Math.multiply")
    self.assertEqual(cmd.arg2, 2)

  def test_return_command_creation(self):
    """Test creating a return command"""
    cmd = Command(
      command_type=CommandType.RETURN,
      arg1=None
    )
    self.assertEqual(cmd.command_type, CommandType.RETURN)
    self.assertIsNone(cmd.arg1)
    self.assertIsNone(cmd.arg2)

  def test_str_arithmetic_command(self):
    """Test string representation of arithmetic commands"""
    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
    self.assertEqual(str(cmd), "add")

    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.SUB)
    self.assertEqual(str(cmd), "sub")

    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.NEG)
    self.assertEqual(str(cmd), "neg")

  def test_str_push_command(self):
    """Test string representation of push commands"""
    cmd = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    self.assertEqual(str(cmd), "push constant 7")

    cmd = Command(CommandType.PUSH, MemorySegment.LCL, 0)
    self.assertEqual(str(cmd), "push local 0")

    cmd = Command(CommandType.PUSH, MemorySegment.ARG, 2)
    self.assertEqual(str(cmd), "push argument 2")

  def test_str_pop_command(self):
    """Test string representation of pop commands"""
    cmd = Command(CommandType.POP, MemorySegment.LCL, 0)
    self.assertEqual(str(cmd), "pop local 0")

    cmd = Command(CommandType.POP, MemorySegment.THAT, 5)
    self.assertEqual(str(cmd), "pop that 5")

  def test_str_branching_command(self):
    cmd = Command(CommandType.BRANCHING, BranchingCommand.IF_GOTO, "LABEL")
    self.assertEqual(str(cmd), "if-goto LABEL")

    cmd = Command(CommandType.BRANCHING, BranchingCommand.GOTO, "LABEL")
    self.assertEqual(str(cmd), "goto LABEL")

    cmd = Command(CommandType.BRANCHING, BranchingCommand.LABEL, "LABEL")
    self.assertEqual(str(cmd), "label LABEL")

  def test_str_function_command(self):
    cmd = Command(CommandType.FUNCTION, "mult", 2)
    self.assertEqual(str(cmd), "function mult 2")

    cmd = Command(CommandType.RETURN, None, None)
    self.assertEqual(str(cmd), "return")

    cmd = Command(CommandType.CALL, "mult", 2)
    self.assertEqual(str(cmd), "call mult 2")

  def test_repr(self):
    """Test repr representation"""
    cmd = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    repr_str = repr(cmd)
    self.assertIn("Command", repr_str)
    self.assertIn("CommandType.PUSH", repr_str)
    self.assertIn("MemorySegment.CONSTANT", repr_str)
    self.assertIn("7", repr_str)

  def test_eq_same_commands(self):
    """Test equality of identical commands"""
    cmd1 = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    cmd2 = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    self.assertEqual(cmd1, cmd2)

  def test_eq_different_commands(self):
    """Test inequality of different commands"""
    cmd1 = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    cmd2 = Command(CommandType.PUSH, MemorySegment.CONSTANT, 8)
    self.assertNotEqual(cmd1, cmd2)

    cmd3 = Command(CommandType.POP, MemorySegment.CONSTANT, 7)
    self.assertNotEqual(cmd1, cmd3)

    cmd4 = Command(CommandType.PUSH, MemorySegment.LCL, 7)
    self.assertNotEqual(cmd1, cmd4)

  def test_eq_with_non_command(self):
    """Test equality with non-Command objects"""
    cmd = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    self.assertNotEqual(cmd, "not a command")
    self.assertNotEqual(cmd, 42)
    self.assertNotEqual(cmd, None)

  def test_is_arithmetic(self):
    """Test is_arithmetic method"""
    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
    self.assertTrue(cmd.is_arithmetic())

    cmd = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    self.assertFalse(cmd.is_arithmetic())

  def test_is_push(self):
    """Test is_push method"""
    cmd = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    self.assertTrue(cmd.is_push())

    cmd = Command(CommandType.POP, MemorySegment.LCL, 0)
    self.assertFalse(cmd.is_push())

    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
    self.assertFalse(cmd.is_push())

  def test_is_pop(self):
    """Test is_pop method"""
    cmd = Command(CommandType.POP, MemorySegment.LCL, 0)
    self.assertTrue(cmd.is_pop())

    cmd = Command(CommandType.PUSH, MemorySegment.CONSTANT, 7)
    self.assertFalse(cmd.is_pop())

    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
    self.assertFalse(cmd.is_pop())

  def test_all_arithmetic_commands(self):
    """Test all arithmetic command types"""
    arithmetic_ops = [
      (ArithmeticCommandTypes.ADD, "add"),
      (ArithmeticCommandTypes.SUB, "sub"),
      (ArithmeticCommandTypes.NEG, "neg"),
      (ArithmeticCommandTypes.EQ, "eq"),
      (ArithmeticCommandTypes.GT, "gt"),
      (ArithmeticCommandTypes.LT, "lt"),
      (ArithmeticCommandTypes.AND, "and"),
      (ArithmeticCommandTypes.OR, "or"),
      (ArithmeticCommandTypes.NOT, "not"),
    ]

    for op, expected_str in arithmetic_ops:
      with self.subTest(op=op):
        cmd = Command(CommandType.ARITHMETIC, op)
        self.assertEqual(str(cmd), expected_str)
        self.assertTrue(cmd.is_arithmetic())

  def test_all_memory_segments(self):
    """Test all memory segment types"""
    segments = [
      MemorySegment.LCL,
      MemorySegment.ARG,
      MemorySegment.THIS,
      MemorySegment.THAT,
      MemorySegment.TEMP,
      MemorySegment.POINTER,
      MemorySegment.STATIC,
      MemorySegment.CONSTANT,
    ]

    for segment in segments:
      with self.subTest(segment=segment):
        cmd = Command(CommandType.PUSH, segment, 0)
        self.assertIn(segment.value, str(cmd))
        self.assertTrue(cmd.is_push())

  def test_str_label_command(self):
    """Test string representation of label command"""
    cmd = Command(CommandType.BRANCHING, BranchingCommand.LABEL, "LOOP_START")
    self.assertEqual(str(cmd), "label LOOP_START")

  def test_str_goto_command(self):
    """Test string representation of goto command"""
    cmd = Command(CommandType.BRANCHING, BranchingCommand.GOTO, "END")
    self.assertEqual(str(cmd), "goto END")

  def test_str_if_goto_command(self):
    """Test string representation of if-goto command"""
    cmd = Command(CommandType.BRANCHING, BranchingCommand.IF_GOTO, "LOOP")
    self.assertEqual(str(cmd), "if-goto LOOP")

  def test_str_function_command(self):
    """Test string representation of function command"""
    cmd = Command(CommandType.FUNCTION, "SimpleFunction.test", 2)
    self.assertEqual(str(cmd), "function SimpleFunction.test 2")

  def test_str_call_command(self):
    """Test string representation of call command"""
    cmd = Command(CommandType.CALL, "Math.multiply", 2)
    self.assertEqual(str(cmd), "call Math.multiply 2")

  def test_str_return_command(self):
    """Test string representation of return command"""
    cmd = Command(CommandType.RETURN, None)
    self.assertEqual(str(cmd), "return")

  def test_is_branching(self):
    """Test is_branching method"""
    cmd = Command(CommandType.BRANCHING, BranchingCommand.LABEL, "TEST")
    self.assertTrue(cmd.is_branching())

    cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
    self.assertFalse(cmd.is_branching())

  def test_is_function(self):
    """Test is_function method"""
    cmd = Command(CommandType.FUNCTION, "Foo.bar", 0)
    self.assertTrue(cmd.is_function())

    cmd = Command(CommandType.CALL, "Foo.bar", 0)
    self.assertFalse(cmd.is_function())

  def test_is_call(self):
    """Test is_call method"""
    cmd = Command(CommandType.CALL, "Foo.bar", 2)
    self.assertTrue(cmd.is_call())

    cmd = Command(CommandType.FUNCTION, "Foo.bar", 2)
    self.assertFalse(cmd.is_call())

  def test_is_return(self):
    """Test is_return method"""
    cmd = Command(CommandType.RETURN, None)
    self.assertTrue(cmd.is_return())

    cmd = Command(CommandType.FUNCTION, "Foo.bar", 0)
    self.assertFalse(cmd.is_return())

  def test_all_branching_commands(self):
    """Test all branching command types"""
    branching_cmds = [
      (BranchingCommand.LABEL, "LABEL_NAME", "label LABEL_NAME"),
      (BranchingCommand.GOTO, "DESTINATION", "goto DESTINATION"),
      (BranchingCommand.IF_GOTO, "LOOP", "if-goto LOOP"),
    ]

    for branch_type, label, expected_str in branching_cmds:
      with self.subTest(branch_type=branch_type):
        cmd = Command(CommandType.BRANCHING, branch_type, label)
        self.assertEqual(str(cmd), expected_str)
        self.assertTrue(cmd.is_branching())

  def test_eq_branching_commands(self):
    """Test equality of branching commands"""
    cmd1 = Command(CommandType.BRANCHING, BranchingCommand.LABEL, "LOOP")
    cmd2 = Command(CommandType.BRANCHING, BranchingCommand.LABEL, "LOOP")
    cmd3 = Command(CommandType.BRANCHING, BranchingCommand.LABEL, "END")

    self.assertEqual(cmd1, cmd2)
    self.assertNotEqual(cmd1, cmd3)

  def test_eq_function_commands(self):
    """Test equality of function commands"""
    cmd1 = Command(CommandType.FUNCTION, "Foo.bar", 2)
    cmd2 = Command(CommandType.FUNCTION, "Foo.bar", 2)
    cmd3 = Command(CommandType.FUNCTION, "Foo.bar", 3)

    self.assertEqual(cmd1, cmd2)
    self.assertNotEqual(cmd1, cmd3)

  def test_eq_return_commands(self):
    """Test equality of return commands"""
    cmd1 = Command(CommandType.RETURN, None)
    cmd2 = Command(CommandType.RETURN, None)
    
    self.assertEqual(cmd1, cmd2)

  def test_function_with_zero_locals(self):
    """Test function declaration with zero local variables"""
    cmd = Command(CommandType.FUNCTION, "Main.main", 0)
    self.assertEqual(str(cmd), "function Main.main 0")

  def test_function_with_multiple_locals(self):
    """Test function declaration with multiple local variables"""
    cmd = Command(CommandType.FUNCTION, "Math.multiply", 5)
    self.assertEqual(str(cmd), "function Math.multiply 5")

  def test_call_with_zero_args(self):
    """Test function call with zero arguments"""
    cmd = Command(CommandType.CALL, "Sys.init", 0)
    self.assertEqual(str(cmd), "call Sys.init 0")

  def test_call_with_multiple_args(self):
    """Test function call with multiple arguments"""
    cmd = Command(CommandType.CALL, "Math.multiply", 2)
    self.assertEqual(str(cmd), "call Math.multiply 2")


if __name__ == '__main__':
  unittest.main()
