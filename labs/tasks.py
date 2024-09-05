import os
import requests
from PIL import Image
import pytesseract
import numpy as np
import cv2
# from background_task import background
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# For Proxy settings
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Set Tesseract path
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Your 2Captcha API key
API_KEY = 'YOUR_2CAPTCHA_API_KEY'

# Set your NopeCHA API key
nopecha.api_key = 'YOUR_API_KEY'


# Function to solve the CAPTCHA using NopeCHA API
def solve_nopecha_captcha(driver):
    # Find the CAPTCHA iframe and switch to it
    captcha_iframe = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
    driver.switch_to.frame(captcha_iframe)

    # Optionally, click the reCAPTCHA checkbox (if visible) to trigger the image selection
    captcha_checkbox = driver.find_element(By.ID, "recaptcha-anchor")
    captcha_checkbox.click()

    # Switch back to the main content to grab CAPTCHA image
    driver.switch_to.default_content()

    # Wait for the CAPTCHA grid to load
    time.sleep(5)

    # Capture CAPTCHA image
    captcha_image = driver.find_element(By.XPATH, "//img[@class='rc-image-tile-44']")
    captcha_image_url = captcha_image.get_attribute('src')

    # Solve the CAPTCHA using NopeCHA
    print("Solving CAPTCHA using NopeCHA API...")

    # Send the image URL to NopeCHA API for solving
    clicks = nopecha.Recognition.solve(
        type='recaptcha',
        task='Select all squares with vehicles.',  # Modify the task as required
        image_urls=[captcha_image_url],
        grid='3x3'  # Adjust the grid size as needed (e.g., '4x4' for larger CAPTCHAs)
    )

    # Print the grid positions that need to be clicked
    print(f"Grid positions to click: {clicks}")

    # Simulate clicks on the corresponding grid positions using Selenium
    for click in clicks:
        row, col = click
        tile_xpath = f"//div[@class='rc-imageselect-tile'][{row * 3 + col + 1}]"
        tile = driver.find_element(By.XPATH, tile_xpath)
        tile.click()

    # Submit the CAPTCHA
    submit_button = driver.find_element(By.ID, "recaptcha-verify-button")
    submit_button.click()

    # Switch back to the main content of the page
    driver.switch_to.default_content()


# Basic CAPTCHA solver using Tesseract OCR
def basic_captcha_solver(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    white_img = cv2.merge([255 - thresh, 255 - thresh, 255 - thresh])
    cv2.imwrite('res/output_image.jpg', white_img)
    image = Image.open('res/output_image.jpg')
    captcha_text = pytesseract.image_to_string(image)
    return captcha_text.strip()


# Solving CAPTCHA by retrieving it and processing the image
def solve_captcha(driver, captcha_image_path):
    captcha_image_element = driver.find_element(By.XPATH, "//img[@id='Imageid']")
    captcha_image_url = captcha_image_element.get_attribute("src")
    captcha_image_response = requests.get(captcha_image_url)

    with open(captcha_image_path, 'wb') as file:
        file.write(captcha_image_response.content)

    extracted_captcha_text = basic_captcha_solver(captcha_image_path)
    return extracted_captcha_text


def solve_2captcha(site_key, url):
    # Request to 2Captcha API to solve reCAPTCHA
    captcha_id = requests.post("http://2captcha.com/in.php", data={
        "key": API_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": url,
        "json": 1
    }).json().get("request")

    # Wait for the CAPTCHA to be solved
    result = None
    while True:
        result = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1").json()
        if result.get("status") == 1:
            print("CAPTCHA solved.")
            return result.get("request")
        print("Waiting for CAPTCHA to be solved...")
        time.sleep(5)


def make_payment(driver):
    try:
        # Enter Card Number
        card_number_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cardNumber"))
        )
        card_number_field.clear()
        card_number_field.send_keys("4111111111111111")

        # Select Expiry Month
        expiry_month_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@data-activates='select-options-eef6ca77-fbf4-eadd-0a90-dee7b31bf2bd']"))
        )
        expiry_month_dropdown.click()

        month_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text(🙁'01']"))
        )
        month_option.click()
    except Exception as e:
        print(f"An Issue occurred while trying to make payment: {e}. Retrying...")


def fill_booking_form(driver):
    captcha_dir = os.path.join(os.getcwd(), "res")
    captcha_image_path = os.path.join(captcha_dir, "captcha_image.jpg")
    max_retries = 5

    for attempt in range(max_retries):
        try:
            # Navigate to Booking Appointment Link
            driver.get("https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment")

            # Wait for the Appointment Form to pop up
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'APPOINTMENT SCHEDULE')]"))
            )

            # Fill the Center location
            center_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "valCenterLocationId"))
            )
            center_dropdown.send_keys("Karachi (Pakistan)")

            # Fill the Service Type
            service_type_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "valCenterLocationTypeId"))
            )
            service_type_dropdown.send_keys("Schengen - Tourist")

            # Fill the Applicant type
            applicant_type_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "valAppointmentForMembers"))
            )
            applicant_type_dropdown.send_keys("Individual")

            # Todo add capcha API : Booking date - Textbased
            # Wait for the user to solve the CAPTCHA
            input("Press Enter after solving the CAPTCHA...")

            # Solve the first CAPTCHA
            # extracted_captcha_text = solve_captcha(driver, captcha_image_path)
            # captcha_input = driver.find_element(By.NAME, "captcha_code")
            # captcha_input.clear()
            # captcha_input.send_keys(extracted_captcha_text)

            # Click on the date dropdown
            date_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "valAppointmentDate"))
            )
            date_dropdown.click()

            # Check for available slots
            available_slots = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//td[contains(@class, 'day') and contains(@class, 'label-available')]")
                )
            )

            if available_slots:
                # Click on the first available slot
                available_slots[0].click()

                print(f"Appointment Time selected { available_slots[0]}")

                # # Select appointment type
                # appointment_type_dropdown = Select(WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.ID, "valApplicationType"))
                # ))
                # appointment_type_dropdown.select_by_visible_text("Normal Time")

                # Wait for the dropdown
                appointment_type_dropdown = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "valAppointmentType"))
                )

                # Scroll the element into view before interacting
                driver.execute_script("arguments[0].scrollIntoView(true);", appointment_type_dropdown)

                # Select "Normal Time" using JavaScript
                driver.execute_script("arguments[0].value = 'normal';", appointment_type_dropdown)
                print("Selected 'Normal Time' as appointment type via JavaScript.")

                # Trigger change event
                driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", appointment_type_dropdown)

                # Continue filling in the rest of the form
                first_name_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "valApplicant[1][first_name]"))
                )
                first_name_input.send_keys("Waqasali")

                # first_name_input = driver.find_element(By.NAME, "valApplicant[1][first_name]")
                # first_name_input.send_keys("Joe")

                last_name_input = driver.find_element(By.NAME, "valApplicant[1][last_name]")
                last_name_input.send_keys("Doe")

                # Todo add capcha API : Booking date - reCaptcha v2
                # Wait for the user to solve the CAPTCHA
                input("Press Enter after solving the reCAPTCHA v2 : Level 3...")


                # Agree to terms and conditions
                agree_checkbox = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "agree"))
                )
                agree_checkbox.click()

                # input("Form filling successful ......")

                # Click the 'Book Now' button Todo: Book appointment
                book_now_button = driver.find_element(By.ID, "valBookNow")
                book_now_button.click()

                print("Booking slot selected and form submitted.")
                return True  # Exit the function if booking is successful


            else:
                print("No available booking slots found.")
                return False

        except Exception as e:
            print(f"An Issue occurred during Filling form attempt {attempt + 1}/{max_retries}: {e}")
            time.sleep(5)  # Wait before retrying
            continue  # Retry the booking process

    print("Max retries reached. Booking process failed.")
    return False


def login(driver):
    captcha_dir = os.path.join(os.getcwd(), "res")
    captcha_image_path = os.path.join(captcha_dir, "captcha_image.jpg")

    while True:  # Loop to handle CAPTCHA retries
        try:
            # Navigate to the login page
            driver.get("https://blsitalypakistan.com/account/login")

            # Directly interact with the elements without waiting
            email_input = driver.find_element(By.XPATH, "//input[@type='text' and @placeholder='Enter Email']")
            email_input.send_keys("Waqasali885875867@gmail.com")


            password_input = driver.find_element(By.NAME, "login_password")
            password_input.send_keys("Azhar2233")

            # Inform the user to manually solve the CAPTCHA
            print("Please solve the CAPTCHA in the browser (select images, etc.)...")

            # Todo add capcha API : Login - reCAPTCHA2
            # Wait for the user to solve the CAPTCHA
            input("Press Enter after solving the CAPTCHA...")

            # Attempt to login after solving CAPTCHA
            login_button = driver.find_element(By.XPATH, "//button[@name='submitLogin']")
            login_button.click()

            # Check if login was successful by inspecting the page content
            time.sleep(5)  # Give some time for the login process to complete

            # Assuming a successful login redirects you to a dashboard or profile page
            if "Profile View" in driver.page_source:
                print("Login Success")
                return True
            else:
                print("Login failed. Retrying...")

        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")


# Initialize the WebDriver
def run_bot_automation():
    captcha_dir = os.path.join(os.getcwd(), "res")
    os.makedirs(captcha_dir, exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    max_retries = 10  # Number of retries if login fails

    for _ in range(max_retries):
        if login(driver):
            # After successful login fill booking form
            fill_booking_form(driver)
            break
        else:
            # Wait before retrying
            time.sleep(5)

    driver.quit()


# Run the automation
run_bot_automation()
