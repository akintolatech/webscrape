import time
from seleniumbase import BaseCase
from credentials import email, password


def fill_booking_form(driver):
    # TO DO: implement booking form filling logic
    pass


def login(driver):
    url = access_link

    try:
        driver.open(url)
        driver.maximize_window()

        # Accepting all cookies in VFS Global website
        acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
        driver.click(acceptcookies_xpath)

        # Wait until email field is visible and fill in
        email_field = "#email"
        driver.send_keys(email_field, email)

        # Fill in password
        password_field = "#password"
        driver.send_keys(password_field, password)

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
    with BaseCase(uc=True, test=True, incognito=True) as driver:
        driver: seleniumbase.BaseCase
        max_retries = 10  # Number of retries if login fails

        for _ in range(max_retries):
            if login(driver):
                # After successful login fill booking form
                fill_booking_form(driver)
                break
            else:
                # Wait before retrying
                time.sleep(5)

