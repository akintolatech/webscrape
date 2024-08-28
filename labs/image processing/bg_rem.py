_image = 'res/des.jpg'
# tesseract_path = 'res/Tesseract-OCR/tesseract.exe'

import cv2
from rembg import remove

# Load the image
input_image_path = 'res/captcha.jpg'  # Replace with your image path
output_image_path = 'res/desbg.png'  # Output path (preferably .png to preserve transparency)

# Read the image
image = cv2.imread(input_image_path)

# Remove the background
output = remove(image)

# Save the output image
cv2.imwrite(output_image_path, output)

print("Background removed and saved as", output_image_path)