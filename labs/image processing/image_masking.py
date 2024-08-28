import cv2
import numpy as np

# Load the image
img = cv2.imread('res/c6.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image to get only black pixels
_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

# Create a 3-channel image with white pixels where threshold is 255
white_img = cv2.merge([255 - thresh, 255 - thresh, 255 - thresh])

# Output the resulting image
cv2.imwrite('output_image.jpg', white_img)
print("Image has been processed successfully!")

# # Display the output image
# cv2.imshow('Output Image', white_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
