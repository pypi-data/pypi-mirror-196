# alienHtml
- A Python package to help with HTML development.

## Install:
```
pip install alienHTML
```
Latest Version:
```
pip install alienHTML==0.0.6
```

## Features:
- Edit or create a HTML file.
- Open HTML files in your browser.
- Print the contents of the HTML file in the shell wth indentation. 
- Add Headings, Images and Pragraphs.

## Example:
```python
from alienHTML import *

# "w" is the mode to open, in this case write. 
mypage = WebPage("/path/to/file/to/create/or/edit", "w", tabhead="Hello World", bgcolour="powderblue",icon="path/to/icon.ico")
# If you put it as "a" it switches to edit mode
# For tabhead, bgcolour and icon, if not set it will automatically set itself to some defaults.

# This creates a heading of the largest size as the number is one.
# It will ask you where you want it in the <body> section of your code
mypage.Heading("Hello World",1)
# Similar for images, just with different parameters. The second is the alt text.
mypage.Image("/path/to/image.png", "Image!")

mypage.showfile() # Prints the contents of the file with line numbers and indentation.
mypage.openpage() # Opens the HTML file in web browser.						             
```
Outputs:

- Ask you where to put code for heading and image.
- Prints the file in shell.
- Opens the page in a web browser

## To do:

- Add more web page features.
- Make the showfile function open the HTML file in web browser, so there is syntax highlighting.

## Credits:

- Made by TomTheCodingGuy