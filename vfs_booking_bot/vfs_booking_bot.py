import os
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

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



def WaitForLoadingToComplete(driver : seleniumbase.BaseCase):
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

# def login(driver):
#
#     while True:  # Loop to handle CAPTCHA retries
#         try:
#
#             # Navigate to the login page
#             driver.get(access_link)
#
#             # Accepting all cookies
#             acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
#
#             # Wait for the cookie button to be visible and click it
#             WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, acceptcookies_xpath))).click()
#             time.sleep(0.5)
#
#             # Getting and updating latest cookies
#             cookies = driver.get_cookies()
#             for cookie in cookies:
#                 driver.add_cookie(cookie)
#
#             time.sleep(5)
#
#             # Wait until the email input field is present
#             email_input = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located(
#                     (By.XPATH, "//input[@type='text' and @placeholder='jane.doe@email.com']"))
#             )
#             email_input.send_keys(email)
#
#             # Wait until the password input field is present
#             password_input = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='** ** ** ** **']"))
#             )
#             password_input.send_keys(password)
#
#             # Inform the user to manually solve the CAPTCHA
#             print("Please solve the CAPTCHA in the browser (select images, etc.)...")
#
#
#             # Wait until the button is present in the DOM
#             button = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign In')]"))
#             )
#
#             # Enable the button using JavaScript if it's disabled
#             driver.execute_script("arguments[0].removeAttribute('disabled')", button)
#
#             # Click the button
#             button.click()
#
#             # Check if login was successful by inspecting the page content
#             time.sleep(5)  # Give some time for the login process to complete
#
#             # Assuming a successful login redirects you to a dashboard or profile page
#             if "Profile View" in driver.page_source:
#                 print("Login Success")
#                 return True
#             else:
#                 print("Login failed. Retrying...")
#
#         except Exception as e:
#             print(f"An error occurred: {e}. Retrying...")


def login(selenium_driver):
    # URL = "https://visa.vfsglobal.com/are/en/ltp/login"
    URL = access_link
    with SB(uc=True, test = True, incognito = True) as driver:
        driver : seleniumbase.BaseCase

        #-------------------- LOGGING SECTION STARTED!! : 0 --------------------
        try:
            # Initializing VFS Global website
            print(f"User Agent: '{driver.get_user_agent()}'")
            driver.maximize_window()
            driver.uc_open_with_reconnect(URL, 25)

            # Accepting all cookies in VFS Global website
            acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
            WaitForLoadingToComplete(driver)
            driver.click(acceptcookies_xpath,timeout=20)
            driver.sleep(0.5)

            # Getting and updating latest cookies to avoid getting spam/blocked
            driver.get_cookies()
            cook = driver.get_cookies()
            driver.add_cookies(cook)

        except Exception as error:
            print(f"Fail to login due to unexpected issue -> '{error}'")
            # messagebox.showerror("Login Issue", message= 'Fail to login due to unexpected issue!')

        # Wait until the email input field is present
                    email_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//input[@type='text' and @placeholder='jane.doe@email.com']"))
                    )
                    email_input.send_keys(email)

                    # Wait until the password input field is present
                    password_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='** ** ** ** **']"))
                    )
                    password_input.send_keys(password)
        Handling captcha (if not solved automatically)
        print("Handling Captcha")
        driver.uc_gui_handle_captcha()

        #Logging in!
        submitbutton_xpath = "//button[contains(@class,'mat-btn-lg')]"
        signin_button = driver.find_element(By.XPATH,submitbutton_xpath)
        signin_button.click()
        WaitForLoadingToComplete(driver)
        print("Clicked Sign In!!!")
        #-------------------- LOGGING SECTION ENDED!!: 0 --------------------

        #-------------------- POST LOGIN SECTION STARTED!!: 1 --------------------
        newbooking_xpath = "//span[contains(.,'Start New Booking')]/parent::button[contains(@class,'d-lg-inline-block')]"


# Initialize the WebDriver
def run_bot_automation():
    # # Launch Chrome in undetected mode
    # # chrome_options = webdriver.ChromeOptions()
    # chrome_options = uc.ChromeOptions()
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--incognito")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Launch Chrome in undetected mode
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")  # Maximize window
    options.add_argument("--incognito")  # Run browser in incognito mode
    options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation
    options.add_argument("--disable-popup-blocking")  # Allow popups
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")  # Optimize performance

    # Initialize undetected Chrome driver
    driver = uc.Chrome(options=options, use_subprocess=True)


    max_retries = 10  # Number of retries if login fails

    for _ in range(max_retries):
        login()
        # if login(driver):
        #     # After successful login fill booking form
        #     # fill_booking_form(driver)
        #     break
        # else:
        #     # Wait before retrying
        #     time.sleep(5)

    driver.quit()


# Run the automation
run_bot_automation()
