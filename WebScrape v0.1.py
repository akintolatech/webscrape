from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



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

    # Manually handle the CAPTCHA (you can pause here until the CAPTCHA is solved)
    input("Please solve the CAPTCHA and press Enter...")

    # Locate and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@name='submitLogin']")
    login_button.click()

    # Optionally, wait for a success element to appear or check for successful login
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//some_element_after_successful_login"))
    # )

    print("Login successful")

except TimeoutException:
    print("Timeout while trying to login")
finally:
    # Close the browser
    driver.quit()
