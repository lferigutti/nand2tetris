from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemorySegment, BranchingCommand
from typing import Union


class Command:
  def __init__(
      self,
      command_type: CommandType,
      arg1: Union[ArithmeticCommandTypes, MemorySegment, BranchingCommand, str, None],
      arg2: Union[None, int, str] = None
  ):
    self.command_type = command_type
    self.arg1 = arg1
    self.arg2 = arg2

  def __str__(self):
    parts = []
    if self.command_type != CommandType.ARITHMETIC and self.command_type != CommandType.BRANCHING:
      parts.append(self.command_type.value)
    if self.command_type != CommandType.RETURN:
      parts.append(self.arg1.value if not isinstance(self.arg1, str) else self.arg1)
    if self.arg2 is not None:
      parts.append(str(self.arg2))
    return ' '.join(parts)

  def __repr__(self):
    return f"Command(command_type={self.command_type!r}, arg1={self.arg1!r}, arg2={self.arg2!r})"

  def __eq__(self, value):
    if not isinstance(value, Command):
      return False
    return (self.command_type == value.command_type and
            self.arg1 == value.arg1 and
            self.arg2 == value.arg2)

  def is_arithmetic(self):
    return self.command_type == CommandType.ARITHMETIC

  def is_branching(self):
    return self.command_type == CommandType.BRANCHING

  def is_function(self):
    return self.command_type == CommandType.FUNCTION

  def is_return(self):
    return self.command_type == CommandType.RETURN

  def is_call(self):
    return self.command_type == CommandType.CALL

  def is_add(self):
    return self.arg1 == ArithmeticCommandTypes.ADD

  def is_sub(self):
    return self.arg1 == ArithmeticCommandTypes.SUB

  def is_eq_lt_gt(self):
    return self.arg1 == ArithmeticCommandTypes.EQ or self.arg1 == ArithmeticCommandTypes.LT or self.arg1 == ArithmeticCommandTypes.GT

  def is_not_neg(self):
    return self.arg1 == ArithmeticCommandTypes.NOT or self.arg1 == ArithmeticCommandTypes.NEG

  def is_and_or(self):
    return self.arg1 == ArithmeticCommandTypes.AND or self.arg1 == ArithmeticCommandTypes.OR

  def is_push(self):
    return self.command_type == CommandType.PUSH

  def is_pop(self):
    return self.command_type == CommandType.POP

  def is_constant_segment(self):
    return self.arg1 == MemorySegment.CONSTANT

  def is_common_segment(self):
    """
    Returns true if the segment is {local, arg, this, that}. This is useful  for translation.
    """
    return self.arg1 == MemorySegment.LCL or self.arg1 == MemorySegment.ARG or self.arg1 == MemorySegment.THIS or self.arg1 == MemorySegment.THAT

  def is_temp_segment(self):
    return self.arg1 == MemorySegment.TEMP

  def is_static_segment(self):
    return self.arg1 == MemorySegment.STATIC

  def is_pointer_segment(self):
    return self.arg1 == MemorySegment.POINTER
