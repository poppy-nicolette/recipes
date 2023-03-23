import os
import pytesseract as ts
from PIL import Image, ImageFilter


def ocr():
    #find all image files in list, jpg or png
    # try except error by pass
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
        #print(text)
        return text
        # part str at \n
        #text_list = text.split('\n')
        text_list=text
    return text_list
    print(text_list)

  #straight from the image as a list of items
  # the list approach keeps the order and relevant tokens together