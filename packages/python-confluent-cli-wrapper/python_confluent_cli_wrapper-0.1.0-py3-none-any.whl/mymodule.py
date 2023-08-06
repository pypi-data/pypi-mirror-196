from mylib.mymodule import MyModule

class MyModule:
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  def __init__(self):
    self.myvar=1
    # self._parser = OutputParser()

  def executeAnything(self):
    return print('anything executed!')
      

