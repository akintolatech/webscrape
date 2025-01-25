import time
from selenium.webdriver.common.by import By
import seleniumbase
from seleniumbase import SB
from credentials import access_link_data
from random import uniform




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

# Utilities
def wait_for_loading_to_complete (driver):
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


def type_string(driver, string: str) -> None:

    keyboard_rows = driver.find_elements('div.touch-keyboard-row')

    for char in string:
        for row in keyboard_rows:
            keys = row.find_elements('button.touch-keyboard-key.standard-key')
            for key in keys:
                if key.text.lower() == char.lower():
                    driver.click(key)
                    break
        # Handle special characters like '@' and '#'
        if char == '@':
            driver.click('button.touch-keyboard-key.function-key')
        elif char == '#':
            driver.click('button.touch-keyboard-key.function-key.numeric-key')

def fill_booking_form(driver):
    # TO DO: implement booking form filling logic
    pass


def login(driver, url, email, password):


    try:
        # driver.open(url)
        driver.uc_open_with_reconnect(url, 25)
        # driver.maximize_window()
        # Set window position and size to dock it to the side
        driver.set_window_position(100, 100)  # x, y coordinates
        driver.set_window_size(800, 600)  # width, height



        # Accepting all cookies in VFS Global website
        acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
        wait_for_loading_to_complete(driver)
        driver.click(acceptcookies_xpath, timeout=20)
        driver.sleep(0.5)

        # Getting and updating latest cookies to avoid getting spam/blocked
        driver.get_cookies()
        cook = driver.get_cookies()
        driver.add_cookies(cook)

        # Wait until email field is visible and fill in
        email_field = "#email"
        driver.send_keys(email_field, email)
        time.sleep(1)

        # Filling the password
        print("Filling Password")
        driver.find_element(By.ID, 'password').send_keys(password)
        time.sleep(3)

        # type_string(driver, password)
        time.sleep(uniform(0, 0.5))

        # Breakpoint
        input("Press Enter to continue")
        #Logging in!
        submitbutton_xpath = "//button[contains(@class,'mat-btn-lg')]"
        driver.click(submitbutton_xpath)

        # Wait for login to complete
        time.sleep(10)

        return True

    except Exception as error:
        print(f"Fail to login due to unexpected issue -> '{error}'")
        return False



def run_vfs_bot():
    with SB(uc=True, test=True, incognito=True) as driver:
        driver : seleniumbase.BaseCase
        max_retries = 10  # Number of retries if login fails

        # Parameters to run the bot against
        key = "qtr-prt"
        url = access_link_data[key][0]
        user_email = access_link_data[key][1]
        user_password = access_link_data[key][2]

        for _ in range(max_retries):
            if login(driver, url, user_email, user_password):
                # After successful login fill booking form
                fill_booking_form(driver)
                break
            else:
                # Wait before retrying
                time.sleep(5)

run_vfs_bot()