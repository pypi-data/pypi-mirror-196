import unittest
from mymodule import MyModule

myModule=MyModule()

class MyModuleTest(unittest.TestCase):
  def setUp(self):
    print('setUp')

  def tearDown(self):
    print('tearDown')

  def test_executeAnything(self):
    myModule.executeAnything()
    self.assertNotEqual(1, None)

if __name__ == '__main__':
  unittest.main(argv=['first-arg-is-ignored'], exit=False)
