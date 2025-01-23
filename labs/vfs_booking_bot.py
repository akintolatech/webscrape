import os
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from random import uniform
from credentials import email, password

import seleniumbase
from seleniumbase import SB

access_link = "https://visa.vfsglobal.com/qat/en/prt/login"

URLS_DICT = {
    "Thailand": "https://visa.vfsglobal.com/tha/en/ltp/login",
    "Dubai": "https://visa.vfsglobal.com/are/en/ltp/login",
    "Malaysia": "https://visa.vfsglobal.com/mys/en/ltp/login",
    "Baku": "https://visa.vfsglobal.com/aze/en/ltp/login"
}

client_details = {
    'Migris': '12345',
    'First Name': 'John',
    'Last Name': 'Doe',
    'DOB': '01/01/1990',
    'Passport Num': 'A12345678',
    'Passport Expiry': '12/12/2030',
    'Ph. Code': '+1',
    'Phone': '1234567890',
    'Email': 'john.doe@example.com',
    'Gender': 'Male',
    'Nationality': 'American'
}


def wait_for_loading_to_complete(driver: seleniumbase.BaseCase):
    loading_path = '//div[@class="ngx-overlay loading-foreground"]'
    i = 1
    while True:
        if driver.is_element_present(loading_path):
            print(f"Loading appears: {i}")
            time.sleep(5)
            i += 1

        else:
            print("Loading Completed")
            break


def login_and_initialize_bot():
    url = access_link

    with SB(uc=True, test = True, incognito = True) as driver:
        driver : seleniumbase.BaseCase

        #-------------------- LOGGING SECTION STARTED!! : 0 --------------------
        try:
            # Initializing VFS Global website
            print(f"User Agent: '{driver.get_user_agent()}'")
            driver.maximize_window()
            driver.uc_open_with_reconnect(url, 25)

            # Accepting all cookies in VFS Global website
            acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
            wait_for_loading_to_complete(driver)
            driver.click(acceptcookies_xpath,timeout=20)
            driver.sleep(0.5)

            # Getting and updating latest cookies to avoid getting spam/blocked
            driver.get_cookies()
            cook = driver.get_cookies()
            driver.add_cookies(cook)

        except Exception as error:
            print(f"Fail to login due to unexpected issue -> '{error}'")
            # messagebox.showerror("Login Issue", message= 'Fail to login due to unexpected issue!')

        # Wait until email field is visible and fill in
        driver.find_element(By.ID, 'email').send_keys(email)
        time.sleep(3)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        # time.sleep(3)

        # Fill in password
        driver.find_element(By.ID, 'password').send_keys(password)
        time.sleep(3)

        #Handling captcha (if not solved automatically)
        # print("Handling Captcha")
        # driver.uc_gui_handle_captcha()

        #Logging in!
        submitbutton_xpath = "//button[contains(@class,'mat-btn-lg')]"
        signin_button = driver.find_element(By.XPATH,submitbutton_xpath)
        signin_button.click()
        wait_for_loading_to_complete(driver)
        print("Clicked Sign In!!!")
        time.sleep(10)
        return True


        #-------------------- LOGGING SECTION ENDED!!: 0 --------------------

        # #-------------------- POST LOGIN SECTION STARTED!!: 1 --------------------
        # newbooking_xpath = "//span[contains(.,'Start New Booking')]/parent::button[contains(@class,'d-lg-inline-block')]"
        # try:
        #     wait_for_loading_to_complete(driver)
        #     driver.wait_for_element_clickable(newbooking_xpath)
        #     print("Login Successful!")
        #     # book_appointment(driver = driver,client_details = client_details)
        # except Exception as error:
        #     print(f"Fail to login due to unexpected issue -> '{error}'")
        #     # messagebox.showerror("Login Issue", message= 'Fail to login due to unexpected issue!')


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
def run_vfs_bot():


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


run_vfs_bot()