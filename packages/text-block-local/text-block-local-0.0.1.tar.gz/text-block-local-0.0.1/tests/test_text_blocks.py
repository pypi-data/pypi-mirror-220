import unittest
from unittest.mock import patch
from CirclesTextBlockLocal.text_blocks import TextBlocks

class TestInsert(unittest.TestCase):
    
    def setUp(self):
      blocks = [(3, 
      '''Sydney Lauer
        sydlauer@umich.edu
        9252853371
        0553083627
        Ann Arbor, Michigan
      '''),  (4,
      '''Sydney Lauer
        0301/2003
        9252853371
        srlauer3103@gmail.com
        March 1 2003
      ''')]
      self.classifier = TextBlocks(blocks)

    @patch('builtins.print')
    def test_extract_fields(self, mock_print):
      fields = self.classifier.extract_fields()
      expected = {'Email': [' sydlauer@umich.edu', ' srlauer3103@gmail.com'], 'Phone Number': [' 9252853371']}
      self.assertDictEqual(fields, expected)
          
if __name__ == '__main__':
    unittest.main()



