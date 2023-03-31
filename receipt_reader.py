"""
reference for pytesseract
https://pypi.org/project/pytesseract/
It may be necessary to specify the tesseract executable on your local path
"""
#!pip install pytesseract

import os
import pytesseract as ts
from PIL import Image, ImageFilter

def ocr():
    #find all image files in list, jpg or png
    path_of_the_directory = os.getcwd()
    ext = ('.jpg', '.png')
    image_list = []
    for files in os.listdir(path_of_the_directory):
        if files.endswith(ext):
            print("Processing:  " + files)
            image_list.append(files)
        else:
            continue

    #create loop that runs through images
    for i in range(len(image_list)):
        img = Image.open(image_list[i])
        img = img.point(lambda p: p > 75 and p + 100)

        #convert image to string
        text=ts.image_to_string(img)
        return text

    return text_list
    print(text_list)

  # the list approach keeps the order and relevant tokens together



