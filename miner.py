import math
import fitz
from tkinter import PhotoImage
from pdf2image import convert_from_path
import img2pdf
import os

from hide_info.analysis import Analysis


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

    def convert_to_pdf(self, img):
        if self.newfilepath:
            with open(self.newfilepath, "wb") as f:
                f.write(img2pdf.convert(img))
        else:
            with open(self.path, "wb") as f:
                f.write(img2pdf.convert(img))
        [os.remove(file) for file in os.listdir(os.curdir) if file.endswith('.jpg')]

    def convert_to_img(self):
        images = convert_from_path(self.path, 355)
        self.convert_to_pdf(Analysis().analysis(images))

