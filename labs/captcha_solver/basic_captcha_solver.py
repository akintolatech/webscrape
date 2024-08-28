from PIL import Image
import pytesseract

import numpy as np
import cv2

_image = 'res/c2.jpg'
tesseract_path = 'res/Tesseract-OCR/tesseract.exe'


def basic_captcha_solver(img_path):

    img = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to get only black pixels
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Create a 3-channel image with white pixels where threshold is 255
    white_img = cv2.merge([255 - thresh, 255 - thresh, 255 - thresh])

    # Output the resulting image
    cv2.imwrite('res/output_image.jpg', white_img)

    # Solve CAPTCHA from output image
    image = Image.open('res/output_image.jpg')
    captcha_text = pytesseract.image_to_string(image)

    return captcha_text.strip()


print(basic_captcha_solver(_image))

