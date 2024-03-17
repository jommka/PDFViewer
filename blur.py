import cv2
import processing


class Blur:

    def __init__(self):
        self.proc = processing.Processing()

    def blur(self, f, position, h):
        img = self.proc.open_image(f)
        rect = img[position[1]:position[1] + h, position[0]:position[2] + position[3]]
        blurred = cv2.blur(rect, (81, 81))
        blurred[:, 0] = 0
        img[position[1]:position[1] + h, position[0]:position[2] + position[3]] = blurred
        cv2.imwrite(f, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))