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

import seleniumbase
from seleniumbase import SB

access_link = "https://visa.vfsglobal.com/qat/en/prt/login"
email = "qatrtarikprt01@mailsac.com"
password = "@T147852a#@"

URLS_DICT = {
    "Thailand": "https://visa.vfsglobal.com/tha/en/ltp/login",
    "Dubai": "https://visa.vfsglobal.com/are/en/ltp/login",
    "Malaysia": "https://visa.vfsglobal.com/mys/en/ltp/login",
    "Baku": "https://visa.vfsglobal.com/aze/en/ltp/login"
}


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

                # Wait for the appointment type dropdown to appear within a reasonable time
                appointment_type_dropdown = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "valAppointmentType"))
                )
                print("Appointment type dropdown found.")

                # Select "Normal Time"
                select = Select(appointment_type_dropdown)
                select.select_by_value("normal")
                print("Selected 'Normal Time' as appointment type.")

                # Continue filling in the rest of the form
                first_name_input = driver.find_element(By.NAME, "valApplicant[1][first_name]")
                first_name_input.send_keys("YourFirstName")

                last_name_input = driver.find_element(By.NAME, "valApplicant[1][last_name]")
                last_name_input.send_keys("YourLastName")

                # # Solve the second CAPTCHA
                # extracted_captcha_text = solve_captcha(driver, captcha_image_path)
                # captcha_input = driver.find_element(By.NAME, "captcha_code")
                # captcha_input.clear()
                # captcha_input.send_keys(extracted_captcha_text)

                # Agree to terms and conditions
                agree_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "agreeTerms"))
                )
                agree_checkbox.click()

                # Click the 'Book Now' button
                book_now_button = driver.find_element(By.ID, "valBookNow")
                book_now_button.click()

                print("Booking slot selected and form submitted.")
                return True  # Exit the function if booking is successful

            else:
                print("No available booking slots found.")
                return False

        except Exception as e:
            print(f"An error occurred during attempt {attempt + 1}/{max_retries}: {e}")
            time.sleep(5)  # Wait before retrying
            continue  # Retry the booking process

    print("Max retries reached. Booking process failed.")
    return False


def WaitForLoadingToComplete(driver: seleniumbase.BaseCase):
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

def login(driver):
    try:
        print(f"User Agent: '{driver.execute_script('return navigator.userAgent;')}'")
        driver.maximize_window()
        driver.get(access_link)

        # Accept cookies
        try:
            acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
            driver.find_element(By.XPATH, acceptcookies_xpath).click()
            print("Accepted cookies.")
            time.sleep(0.5)
        except Exception as e:
            print(f"Cookies button not found: {e}")

        # Fill in credentials
        driver.find_element(By.ID, 'email').send_keys(email)
        time.sleep(0.5)
        driver.find_element(By.ID, 'password').send_keys(password)
        time.sleep(0.5)

        # Handle captcha manually (or implement automation here)
        print("Handle Captcha manually if required...")

        # Submit login form
        submitbutton_xpath = "//button[contains(@class,'mat-btn-lg')]"
        driver.find_element(By.XPATH, submitbutton_xpath).click()
        time.sleep(5)  # Wait for login process

        print("Login successful.")

        # Check if login is successful
        if "dashboard" in driver.current_url:
            return True
        else:
            return False

    except Exception as error:
        print(f"Login failed: {error}")
        return False

def run_bot_automation():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options, use_subprocess=True)
    max_retries = 5

    for _ in range(max_retries):
        if login(driver):
            print("Proceeding to next step...")
            break
        else:
            print("Retrying login...")
            time.sleep(5)

    driver.quit()

# Run the automation
run_bot_automation()

# def login():
#     # URL = "https://visa.vfsglobal.com/are/en/ltp/login"
#     URL = access_link
#     with SB(uc=True, test=True, incognito=True) as driver:
#         driver: seleniumbase.BaseCase
#
#         # -------------------- LOGGING SECTION STARTED!! : 0 --------------------
#         try:
#             # Initializing VFS Global website
#             print(f"User Agent: '{driver.get_user_agent()}'")
#             driver.maximize_window()
#             driver.uc_open_with_reconnect(URL, 25)
#
#             # Accepting all cookies in VFS Global website
#             acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
#             WaitForLoadingToComplete(driver)
#             driver.click(acceptcookies_xpath, timeout=20)
#             print("Accepted cookies ....................................... OK")
#             driver.sleep(0.5)
#
#             # Getting and updating latest cookies to avoid getting spam/blocked
#             driver.get_cookies()
#             cook = driver.get_cookies()
#             driver.add_cookies(cook)
#
#         except Exception as error:
#             print(f"Fail to login due to unexpected issue -> '{error}'")
#             # messagebox.showerror("Login Issue", message= 'Fail to login due to unexpected issue!')
#
#         # Filling the email
#         print("Filling Username")
#         email_input = driver.find_element(By.ID, 'email')
#         # for email_key in EMAIL:
#         email_input.send_keys(email)
#         time.sleep(uniform(0, 0.5))
#
#         # Filling the password
#         print("Filling Password")
#         password_input = driver.find_element(By.ID, 'password')
#         # for pass_key in PASSWORD:
#         password_input.send_keys(password)
#         time.sleep(uniform(0, 0.5))
#
#         # Handling captcha (if not solved automatically)
#         print("Handling Captcha")
#         driver.uc_gui_handle_captcha()
#
#         # Logging in!
#         submitbutton_xpath = "//button[contains(@class,'mat-btn-lg')]"
#         signin_button = driver.find_element(By.XPATH, submitbutton_xpath)
#         signin_button.click()
#         WaitForLoadingToComplete(driver)
#         print("Clicked Sign In!!!")
#         # -------------------- LOGGING SECTION ENDED!!: 0 --------------------
#
#         # -------------------- POST LOGIN SECTION STARTED!!: 1 --------------------
#         newbooking_xpath = "//span[contains(.,'Start New Booking')]/parent::button[contains(@class,'d-lg-inline-block')]"
#         print("Login successful.................")
#
#
# # Initialize the WebDriver in a seleniumbase undetected mode
# def run_bot_automation():
#     # # Launch Chrome in undetected mode
#     # # chrome_options = webdriver.ChromeOptions()
#     # chrome_options = uc.ChromeOptions()
#     # chrome_options.add_argument("--start-maximized")
#     # chrome_options.add_argument("--incognito")
#     # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#
#     # Launch Chrome in undetected mode
#     options = uc.ChromeOptions()
#     options.add_argument("--start-maximized")  # Maximize window
#     options.add_argument("--incognito")  # Run browser in incognito mode
#     options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation
#     options.add_argument("--disable-popup-blocking")  # Allow popups
#     options.add_argument("--no-first-run --no-service-autorun --password-store=basic")  # Optimize performance
#
#     # Initialize undetected Chrome driver
#
#     driver = uc.Chrome(options=options, use_subprocess=True)
#
#     max_retries = 10  # Number of retries if login fails
#
#     for _ in range(max_retries):
#         login()
#         # if login(driver):
#         #     # After successful login fill booking form
#         #     # fill_booking_form(driver)
#         #     break
#         # else:
#         #     # Wait before retrying
#         #     time.sleep(5)
#
#     driver.quit()


# Run the automation
run_bot_automation()
