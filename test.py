class test(object):
 def __init__(self, **kwargs):
  print(kwargs)
 a=10
 b=20
 c=100
 def tes(self):
  print(self.a, self.b)

test().__dict__
