from typing import List

from vm_translator.src.command import Command
from vm_translator.src.assembly_expressions import AssemblyExpressions


class VMTranslator:
  assembly_expressions = AssemblyExpressions()

  def __init__(self, file_name: str):
    self.label_counter = 0
    self.file_name = file_name

  def translate(self, commands: List[Command], write_comment: bool = True) -> List[str]:
    output = []
    for command in commands:
      if write_comment:
        comment = f"// {str(command)}"
        output.append(comment)
      command_translated = self._translate_command(command)
      output.extend(command_translated)
    return output

  def _translate_command(self, command: Command) -> List[str]:
    if command.is_arithmetic():
      return self._translate_arithmetic_command(command)
    elif command.is_push():
      return self._translate_push_command(command)
    elif command.is_pop():
      return self._translate_pop_command(command)
    else:
      raise NotImplemented(f"Command {command.command_type} not implemented yet.")

  def _translate_arithmetic_command(self, command: Command) -> List[str]:
    if command.is_add():
      return ["@SP", "A=M-1", "D=M", "A=A-1", "M=D+M", "@SP", "M=M-1"]
    elif command.is_sub():
      return ["@SP", "A=M-1", "D=M", "A=A-1", "M=M-D", "@SP", "M=M-1"]
    elif command.is_eq_lt_gt():
      self.label_counter += 1
      jump_command = self.assembly_expressions.jump(command.arg1)
      return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", f"@{command.arg1.value.upper()}_TRUE_{self.label_counter}",
              f"D;{jump_command}", "@SP",
              "A=M-1", "M=0", f"@END_{self.label_counter}", "0;JMP",
              f"({command.arg1.value.upper()}_TRUE_{self.label_counter})",
              "@SP", "A=M-1",
              "M=-1", f"(END_{self.label_counter})"]
    elif command.is_not_neg():
      operation = self.assembly_expressions.get_operation(command.arg1)
      return ["@SP", "A=M-1", f"M={operation}M"]
    elif command.is_and_or():
      operation = self.assembly_expressions.get_operation(command.arg1)
      return ["@SP", "AM=M-1", "D=M", "A=A-1", f"M=D{operation}M"]
    else:
      raise SyntaxError(f"Arithmetic Command '{str(command)}' is not valid. Arg {command.arg1} does not exist.")

  def _translate_push_command(self, command: Command) -> List[str]:
    if command.is_constant_segment():
      return [f'@{command.arg2}', "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif command.is_common_segment() or command.is_temp_segment():
      segment = self.assembly_expressions.segment(command.arg1)
      value = "M" if command.is_common_segment() else 'A'
      return [f"@{segment}", f"D={value}", f"@{command.arg2}", "A=D+A", "D=M", "@SP", "M=M+1", "A=M-1", "M=D"]
    elif command.is_static_segment():
      return [f"@{self.file_name}.{command.arg2}", "D=M", "@SP", "M=M+1", "A=M-1", "M=D"]
    elif command.is_pointer_segment():
      segment = self.assembly_expressions.get_pointer_mapping(command.arg2)
      return [f"@{segment}", "D=M", "@SP", "M=M+1", "A=M-1", "M=D"]
    else:
      raise SyntaxError(f"Push Command '{str(command)}' is not valid. Segment {command.arg1} does not exist.")

  def _translate_pop_command(self, command: Command) -> list[str]:
    if command.is_common_segment() or command.is_temp_segment():
      segment = self.assembly_expressions.segment(command.arg1)
      value = "M" if command.is_common_segment() else 'A'
      return [f"@{segment}", f"D={value}", f"@{command.arg2}", "D=D+A", "@SP", "M=M-1", "A=M+1", "M=D", "A=A-1", "D=M",
              "A=A+1", "A=M", "M=D"]
    elif command.is_static_segment():
      return [f"@{self.file_name}.{command.arg2}", "D=A", "@SP", "M=M-1", "A=M+1", "M=D", "A=A-1", "D=M",
              "A=A+1", "A=M", "M=D"]
    elif command.is_pointer_segment():
      segment = self.assembly_expressions.get_pointer_mapping(command.arg2)
      return ["@SP", "AM=M-1", "D=M", f"@{segment}", "M=D"]
    else:
      raise SyntaxError(f"Pop Command '{str(command)}' is not valid. Segment {command.arg1} does not exist.")
