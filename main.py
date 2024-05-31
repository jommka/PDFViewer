from tkinter import *
from viewer import Viewer
import os,argparse

if __name__ == '__main__':
    root = Tk()
    app = Viewer(root)
    root.mainloop()


from pytesseract import pytesseract
from PIL import Image
import re
import cv2
from hide_info.regex import Regex
from pdf2image import convert_from_path


# title = 'obrazec'

# конвертация в изображения (затратно по времени)
# images = convert_from_path(f'{title}.pdf', 700)
# for i, image in enumerate(images):
#     image.save(f'save_{i}.png')
#


# чтение с изображения (быстро)
# path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# pytesseract.tesseract_cmd = path_to_tesseract
#
# img = cv2.imread('example.jpg', cv2.IMREAD_COLOR)  # Open the image from which charectors has to be recognized
# # img = cv2.resize(img, (620,480) ) #resize the image if required
#
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey to reduce detials
# gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
#
# text = pytesseract.image_to_string(gray, config='-l rus')
# # test = (pytesseract.image_to_data(gray, lang=None, config='', nice=0) ) #get confidence level if required
# # print(pytesseract.image_to_boxes(gray))
# #
# print(text)
#
#
# # получение регулярных выражений
# regex_dict = Regex().get_pattern()
# print(regex_dict)






