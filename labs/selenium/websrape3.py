from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def login_and_extract_text(email, password):
    try:
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")  # Start browser maximized
        chrome_options.add_argument("--disable-notifications")  # Disable notifications
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")  # Run in headless mode if you don't want the browser GUI

        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 20)  # Explicit wait of 20 seconds

        # Navigate to the login page
        login_url = 'https://blsitalypakistan.com/account/login'
        driver.get(login_url)

        # Fill in the email field
        email_field = wait.until(EC.presence_of_element_located((By.NAME,
                                                                 'b2528159098bb82b1d4b1bd91c3d7ef263583824f153f85651419522b2357bdad3ced39589f148d833838a8fc75718af1aa655b68d18c3cdc2169063cc8ee2b3nUDFtO+6WvU5B4VktviCnISLvBaBapFgs9ygZBnLkzM=')))
        email_field.clear()
        email_field.send_keys(email)

        # Fill in the password field
        password_field = driver.find_element(By.NAME, 'login_password')
        password_field.clear()
        password_field.send_keys(password)

        # Handle captcha
        captcha_image = driver.find_element(By.ID, 'Imageid')
        captcha_src = captcha_image.get_attribute('src')
        captcha_filename = 'captcha.png'
        captcha_image.screenshot(captcha_filename)
        print(f"Captcha image saved as '{captcha_filename}'. Please open the image and enter the captcha code.")

        # Open captcha image automatically (optional, works on some OS)
        try:
            os.startfile(captcha_filename)
        except:
            pass  # If not supported, user can open manually

        captcha_code = input("Enter Captcha: ")

        # Enter captcha code
        captcha_field = driver.find_element(By.NAME, 'captcha_code')
        captcha_field.clear()
        captcha_field.send_keys(captcha_code)

        # Submit the login form
        submit_button = driver.find_element(By.NAME, 'submitLogin')
        submit_button.click()

        # Wait until the page loads and a specific element is present to confirm successful login
        # Adjust the locator according to the page you expect after login
        dashboard_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Extract all text from the page body
        page_text = dashboard_element.text

        print("\nExtracted Text from the Page:\n")
        print(page_text)

        # Optional: Save the text to a file
        with open('extracted_text.txt', 'w', encoding='utf-8') as file:
            file.write(page_text)
        print("\nText has been saved to 'extracted_text.txt'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup: Close the browser and remove captcha image
        driver.quit()
        if os.path.exists(captcha_filename):
            os.remove(captcha_filename)


# Usage
if __name__ == "__main__":
    user_email = 'your_email@example.com'  # Replace with your email
    user_password = 'your_password'  # Replace with your password
    login_and_extract_text(user_email, user_password)
