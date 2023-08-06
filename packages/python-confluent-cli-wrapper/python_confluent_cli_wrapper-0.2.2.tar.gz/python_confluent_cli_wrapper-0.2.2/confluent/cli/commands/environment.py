from subprocess import Popen, PIPE
import shlex
from confluent.cli.commands.login import confluent_cli
from confluent.cli.utils.parsers import OutputParser, OutputEnum

class Environment:
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  def __init__(self):
    self._parser = OutputParser()

  def list(self, parse: bool = True, output: OutputEnum = OutputEnum.human):
    command_line = f'{confluent_cli} environment list --output {output.name}'
    args = shlex.split(command_line)
    pipe = Popen(args=args, stdout=PIPE)
    result = pipe.communicate()
    
    if(not parse): return result
    
    return self._parser.parseOutput(result, output)
      

