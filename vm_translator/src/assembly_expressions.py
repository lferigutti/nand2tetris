from vm_translator.src.models import MemorySegment, ArithmeticCommandTypes


class AssemblyExpressions:
  segment_strings_mapping = {
    MemorySegment.ARG: 'ARG',
    MemorySegment.LCL: 'LCL',
    MemorySegment.THIS: 'THIS',
    MemorySegment.THAT: 'THAT',
    MemorySegment.TEMP: '5'
  }

  jump_command_mapping = {
    ArithmeticCommandTypes.EQ: "JEQ",
    ArithmeticCommandTypes.LT: "JLT",
    ArithmeticCommandTypes.GT: "JGT"
  }

  @staticmethod
  def load_constant(constant: int):
    return [f'@{constant}', "D=A"]

  def segment(self, segment: MemorySegment):
    segment = self.segment_strings_mapping.get(segment)
    if not segment:
      raise SyntaxError(f"The segment {segment} does not exist")
    return segment

  def jump(self, logical_operator: ArithmeticCommandTypes):
    jump_command = self.jump_command_mapping.get(logical_operator)
    if not jump_command:
      raise SyntaxError(f"The logical operator {logical_operator} does not exist.")
    return jump_command

  def get_pointer_mapping(self, value: int):
    if value != 1 and value != 0:
      raise SyntaxError(f"Pointer can be only 0 or 1. You supplied {value}")
    return self.segment_strings_mapping.get(MemorySegment.THAT if value else MemorySegment.THIS)

  @staticmethod
  def get_operation(operand: ArithmeticCommandTypes):
    if operand == ArithmeticCommandTypes.NOT:
      return "!"
    elif operand == ArithmeticCommandTypes.NEG:
      return "-"
    elif operand == ArithmeticCommandTypes.AND:
      return "&"
    elif operand == ArithmeticCommandTypes.OR:
      return "|"
    else:
      raise SyntaxError(f"Operand {operand} does not exist.")
