import os
import cv2
from PIL import Image
from pdf2image import convert_from_path


class Processing:

    @staticmethod
    def convert_to_jpg(path):
        pdfs = path
        os.mkdir("images")
        pages = convert_from_path(pdfs, 355)
        i = 1
        for page in pages:
            image_name = "page_" + str(i) + ".jpg"
            page.save(image_name, "JPEG")
            os.replace(image_name, "images/" + image_name)
            i = i + 1

    @staticmethod
    def convert_to_pdf(lst, path):
        images = [
            Image.open(f)
            for f in lst
        ]
        images[0].save(
            path, resolution=100.0, save_all=True, append_images=images[1:]
        )

    @staticmethod
    def open_image(image):
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    @staticmethod
    def delete_jpg():
        path = './images'
        if os.path.isdir(path):
            for f in os.listdir(path):
                os.remove(os.path.join(path, f))

            os.rmdir("images")
