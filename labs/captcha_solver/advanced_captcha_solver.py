# CAPTCHA Solver with more advanced image processing
from PIL import Image
import pytesseract

import numpy as np
import cv2

_image = 'res/c2.jpg'
tesseract_path = 'res/Tesseract-OCR/tesseract.exe'


def advanced_captcha_solver(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    # Apply adaptive thresholding to deal with different lighting conditions
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Use dilation to fill in gaps between characters
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Save and use OCR to read the CAPTCHA
    processed_img_path = 'res/processed_captcha.jpg'
    cv2.imwrite(processed_img_path, dilated)
    image = Image.open(processed_img_path)
    captcha_text = pytesseract.image_to_string(image, config='--psm 8')

    return captcha_text.strip()