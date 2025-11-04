from vm_translator.src.models import MemorySegment


class AssemblyExpressions:
  segment_strings_mapping = {
    MemorySegment.ARG: 'ARG',
    MemorySegment.LCL: 'LCL',
    MemorySegment.THIS: 'THIS',
    MemorySegment.THAT: 'THAT',
    MemorySegment.TEMP: '5'
  }

  @staticmethod
  def load_constant(constant: int):
    return [f'@{constant}', "D=A"]

  def segment(self, segment):
    segment = self.segment_strings_mapping.get(segment)
    if not segment:
      raise SyntaxError(f"The segment {segment} does not exist")
    return segment

  def get_pointer_mapping(self, value: int):
    if value != 1 and value != 0:
      raise SyntaxError(f"Pointer can be only 0 or 1. You supplied {value}")
    return self.segment_strings_mapping.get(MemorySegment.THAT if value else MemorySegment.THIS)
