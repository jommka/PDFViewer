import math
import fitz
from tkinter import PhotoImage
from pdf2image import convert_from_path
import img2pdf
from pytesseract import pytesseract
from hide_info.regex import Regex
import cv2
import os
import re


class PDFMiner:
    def __init__(self, filepath, newfilepath):
        self.text = None
        self.name_img = None
        self.path = filepath
        self.newfilepath = newfilepath
        self.pdf = fitz.open(filepath)
        self.first_page = self.pdf.load_page(0)
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height
        zoomdict = {800: 0.8, 700: 0.6, 600: 1.0, 500: 1.0}
        width = int(math.floor(self.width / 100.0) * 100)
        self.zoom = zoomdict[width]
        pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def get_metadata(self):
        metadata = self.pdf.metadata
        numPages = self.pdf.page_count
        return metadata, numPages

    def get_page(self, page_num):
        page = self.pdf.load_page(page_num)
        if self.zoom:
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat)
        else:
            pix = page.get_pixmap()
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        imgdata = px1.tobytes("ppm")
        return PhotoImage(data=imgdata)

    # def get_text(self, page_num):
    #     page = self.pdf.load_page(page_num)
    #     text = page.getText('text')
    #     return text
    # COLOR_BGR2GRAY
    # , cv2.IMREAD_COLOR
    @staticmethod
    def open_image(title):
        img = cv2.imread(title, cv2.IMREAD_COLOR)  # Open the image from which charectors has to be recognized
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey to reduce detials
        return gray
        # img = cv2.imread(title)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # return img

    def get_text(self):
        # gray = self.open_image(self.name_img)
        gray = cv2.bilateralFilter(self.open_image(self.name_img), 11, 17, 17)  # Blur to reduce noise
        text = pytesseract.image_to_data(gray, output_type='dict', lang='rus')
        # img = self.open_image(self.name_img)
        # text = pytesseract.image_to_data(img, output_type='dict', config=r'--oem 3 --psm 6', lang='rus')
        return text
        # text_2 = pytesseract.image_to_string(gray, output_type='dict', config='-l rus --oem 3 --psm 6')
        # print(text_2)

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
        print(lst)
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

    def convert_to_pdf(self, img):
        if self.newfilepath:
            with open(self.newfilepath, "wb") as f:
                f.write(img2pdf.convert(img))
        else:
            with open(self.path, "wb") as f:
                f.write(img2pdf.convert(img))
        [os.remove(file) for file in os.listdir(os.curdir) if file.endswith('.jpg')]

    def convert_to_img(self):
        out_img = []
        images = convert_from_path(self.path, 355)
        for i, image in enumerate(images):
            self.name_img = f'save_{i}.jpg'
            image.save(self.name_img)
            text = self.get_text()
            boxes = len(text['level'])
            self.search(text, boxes)
            out_img.append(self.name_img)
        self.convert_to_pdf(out_img)

