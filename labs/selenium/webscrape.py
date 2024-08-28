import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract

# Path to the ChromeDriver and Tesseract OCR executable
chrome_driver_path = '/path/to/chromedriver'
tesseract_path = '../image processing/res/Tesseract-OCR/tesseract.exe'

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


# Function to solve CAPTCHA
def solve_captcha(image_path):
    image = Image.open(image_path)
    captcha_text = pytesseract.image_to_string(image)
    return captcha_text.strip()


# Log in to the target website
def login(username, password):
    login_url = "https://blsitalypakistan.com/login"
    driver.get(login_url)

    # Find username, password fields and CAPTCHA
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    captcha_image = driver.find_element(By.ID, "captcha_image")

    # Fill in credentials
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Solve CAPTCHA
    captcha_image.screenshot("captcha.png")
    captcha_text = solve_captcha("captcha.png")
    captcha_field = driver.find_element(By.NAME, "captcha")
    captcha_field.send_keys(captcha_text)

    # Submit the form
    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()

    # Wait for login to complete and dashboard to load
    time.sleep(5)


# Extract data from dashboard
def extract_dashboard_data():
    dashboard_url = "https://example.com/dashboard"
    driver.get(dashboard_url)

    # Locate and extract the data you need
    data_element = driver.find_element(By.XPATH, "//div[@class='dashboard-data']")
    data_text = data_element.text

    return data_text


# Main function
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    username = "your_username"
    password = "your_password"

    login(username, password)
    dashboard_data = extract_dashboard_data()
    print("Extracted Data:", dashboard_data)

    # Close the driver
    driver.quit()
