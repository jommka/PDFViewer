import re
import os

import blur
import regex
import processing

from pytesseract import pytesseract


class Analysis:
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract

    def __init__(self):
        self.proc = processing.Processing()
        self.reg = regex.Regex()
        self.bl = blur.Blur()

    def read_image(self, name_image):
        img = self.proc.open_image(name_image)
        text = pytesseract.image_to_data(img, output_type='dict', config=r'--oem 3 --psm 6', lang='rus')
        return text

    def pattern(self, f, reg):
        text = self.read_image(f)
        name = re.findall(reg, " ".join(text['text']))
        return name

    @staticmethod
    def text_processing(word):
        res = word.translate(dict.fromkeys(map(ord, u"!;_\\/|")))
        return res.rstrip(",")

    def detection(self, word, boxes, data):
        lst = []
        j = 0
        res = self.text_processing(word).split()

        for level in range(boxes):
            if len(res) != len(lst):
                data['text'][level] = self.text_processing(data['text'][level])
                if data['text'][level]:
                    if j < len(res) and data['text'][level] == self.text_processing(res[j]):
                        lst.append(level)
                        j += 1
                    else:
                        j = 0
                        lst.clear()
            else:
                return lst

    def get_coordinates(self, word, boxes, data):
        lst = self.detection(word, boxes, data)

        if lst:
            coordinates = [data['left'][lst[0]], data['top'][lst[0]], data['left'][lst[-1]], data['width'][lst[-1]]]
            h = data['height'][lst[0]] + 5
            return coordinates, h

    def word_search(self):
        lst_image = []
        regex_dict = self.reg.get_pattern()

        os.chdir("images")

        for f in os.listdir():
            for key in regex_dict:
                data = self.read_image(f)
                boxes = len(data['level'])
                word = self.pattern(f, regex_dict[key])
                for w in word:
                    coordinates, h = self.get_coordinates(w, boxes, data)
                    self.bl.blur(f, coordinates, h)
            lst_image.append(f)
        return lst_image
