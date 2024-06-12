import cv2
import re
from pytesseract import pytesseract

from hide_info.regex import Regex


class Analysis:
    def __init__(self):
        self.name_img = None
        pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    @staticmethod
    def open_image(title):
        img = cv2.imread(title, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        return gray

    def get_text(self):
        gray = self.open_image(self.name_img)
        text = pytesseract.image_to_data(gray, output_type='dict', lang='rus')
        return text

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
        # print(lst)
        if lst:
            coordinates = [data['left'][lst[0]], data['top'][lst[0]], data['left'][lst[-1]], data['width'][lst[-1]]]
            h = data['height'][lst[0]] + 5
            return coordinates, h

    def hide(self, position, h):
        img = self.open_image(self.name_img)
        rect = img[position[1]:position[1] + h, position[0]:position[2] + position[3]]
        blurred = cv2.blur(rect, (81, 81))
        blurred[:, 0] = 0
        img[position[1]:position[1] + h, position[0]:position[2] + position[3]] = blurred
        cv2.imwrite(self.name_img, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    def search(self, text, boxes):
        regex_dict = Regex().get_pattern()
        words = [w for key in regex_dict for w in re.findall(regex_dict[key], " ".join(text['text']))]
        for w in words:
            # print(w)
            coordinates, h = self.get_coordinates(w, boxes, text)
            self.hide(coordinates, h)

    def analysis(self, images):
        out_img = []
        for i, image in enumerate(images):
            self.name_img = f'save_{i}.jpg'
            image.save(self.name_img)
            text = self.get_text()
            boxes = len(text['level'])
            self.search(text, boxes)
            out_img.append(self.name_img)
        return out_img
