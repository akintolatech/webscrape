from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os
import requests

# Captcha processing
from PIL import Image
import pytesseract
import numpy as np
import cv2
import time

# # Replace with the path to your WebDriver (e.g., chromedriver)
# driver_path = 'path_to_your_webdriver'
# driver = webdriver.Chrome(executable_path=driver_path)

# Set up Chrome options if needed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start browser maximized

# Create an instance of the WebDriver (for Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

input_email = "Waqasali885875867@gmail.com"
input_password = "Azhar2233"

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


try:
    # Navigate to the login page
    driver.get("https://blsitalypakistan.com/account/login")

    # Wait until the email input field is present
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='Enter Email']"))
    )

    # Send the email (replace 'your_email' with your actual email)
    email_input.send_keys(input_email)

    # Locate the password input field and enter the password
    password_input = driver.find_element(By.NAME, "login_password")
    password_input.send_keys(input_password)

    # CAPTCHA HANDLING
    # Locate the CAPTCHA image element
    captcha_image_element = driver.find_element(By.XPATH, "//img[@id='Imageid']")

    # Get the CAPTCHA image URL
    captcha_image_url = captcha_image_element.get_attribute("src")

    # Download the CAPTCHA image
    captcha_image_response = requests.get(captcha_image_url)

    # Save the image to a file
    captcha_image_path = os.path.join(os.getcwd(), "res/captcha_image.jpg")
    with open(captcha_image_path, 'wb') as file:
        file.write(captcha_image_response.content)

    # print(f"CAPTCHA image downloaded and saved as {captcha_image_path}")

    extracted_captcha_text = basic_captcha_solver(captcha_image_path)

    # Input CAPTCHA text
    captcha_input = driver.find_element(By.NAME, "captcha_code")
    captcha_input.send_keys(extracted_captcha_text)

    # Locate and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@name='submitLogin']")
    login_button.click()

    # Optionally, wait for a success element to appear or check for successful login
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//some_element_after_successful_login"))
    # )

    print("Login successful")

    # Get all the text from the page
    page_text = driver.find_element(By.TAG_NAME, "body").text

    # Print the text
    print(page_text)

except TimeoutException:
    print("Timeout while trying to login")
finally:
    # Close the browser
    driver.quit()
