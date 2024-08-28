
from PIL import Image
import pytesseract

import numpy as np
import cv2

_image = 'res/in_2.jpg'
tesseract_path = 'res/Tesseract-OCR/tesseract.exe'


# Function to solve CAPTCHA
def solve_captcha(image_path):
    image = Image.open(image_path)
    captcha_text = pytesseract.image_to_string(image)
    return captcha_text.strip()


print("Solved:", solve_captcha(_image))
