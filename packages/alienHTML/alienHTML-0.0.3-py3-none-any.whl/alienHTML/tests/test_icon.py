#########################
# Test default tab icon #
#########################

import unittest
from alienHTML import WebPage

class TestIconWebPage(unittest.TestCase):
    def setUp(self):
        self.mypage = WebPage("./test.html","w",bgcolour="powderblue")
    
    def test_icon(self):
        self.assertEqual
        
 
def cleanup():
    import os
    os.remove("./test.html")