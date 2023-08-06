##########################
# Test WebPage functions #
##########################

import unittest
import urllib
from PIL import Image
from alienHTML import WebPage

class WebPageError(Exception):
    def __init__(self,message="Could not load webpage"):
        self.message=message
        super().__init__(self.message)

class TestWebPage(unittest.TestCase):
    def setUp(self):
        self.mypage = WebPage("test.html","w",bgcolour="powderblue")
    
    def test_init(self):
        self.assertEqual(self.mypage.file,"test.html")
        self.assertEqual(self.mypage.action, "w")
        self.assertEqual(self.mypage.tabhead, "HTML with Python!")
        self.assertEqual(self.mypage.bgcolour, "background-color:powderblue")
        
        urllib.request.urlretrieve('https://raw.githubusercontent.com/TomTheCodingGuy/alienHTML/main/alien_hurt.ico',"alien_hurt.ico")
        self.assertEqual(self.mypage.icon, Image.open("alien_hurt.ico"))
    
    def test_showfile(self):
        __openfile = open("./test.html","rt")
        self.__lines = __openfile.readlines()
        self.assertEqual(self.__lines, self.mypage.showfile())
        cleanup()

def cleanup():
    import os
    os.remove("./test.html")
    if os.path.exists("./alien_hurt.ico"):
        os.remove("./alien_hurt.ico")

def run():
    unittest.main()