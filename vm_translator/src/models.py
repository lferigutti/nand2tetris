from enum import Enum


class CommandType(Enum):
  ARITHMETIC = "arithmetic"
  PUSH = 'push'
  POP = 'pop'
  BRANCHING = 'branching'
  FUNCTION = 'function'
  CALL = 'call'
  RETURN = 'return'


class ArithmeticCommandTypes(Enum):
  ADD = 'add'
  SUB = 'sub'
  NEG = 'neg'
  EQ = 'eq'
  GT = 'gt'
  LT = 'lt'
  AND = 'and'
  OR = 'or'
  NOT = 'not'


class MemoryCommand(Enum):
  PUSH = 'push'
  POP = 'pop'


class BranchingCommand(Enum):
  LABEL = 'label'
  GOTO = 'goto'
  IF_GOTO = 'if-goto'


class MemorySegment(Enum):
  SP = 'SP'
  LCL = 'local'
  ARG = 'argument'
  THIS = 'this'
  THAT = 'that'
  TEMP = 'temp'
  POINTER = 'pointer'
  STATIC = 'static'
  CONSTANT = 'constant'
