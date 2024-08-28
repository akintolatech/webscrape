from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Set up Chrome options if needed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start browser maximized

# Create an instance of the WebDriver (for Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the login page
driver.get('https://sbrsrp.pythonanywhere.com/')

# Find the email field and input your email
email_field = driver.find_element(By.NAME, 'username')
email_field.send_keys('admin')

# Find the password field and input your password
password_field = driver.find_element(By.NAME, 'password')
password_field.send_keys('adminmaster')

# # Handle captcha manually or use a third-party service to solve it
# captcha_field = driver.find_element(By.NAME, 'captcha_code')
# captcha_image = driver.find_element(By.ID, 'Imageid')
#
# # Save the captcha image to manually solve it (if necessary)
# captcha_image.screenshot('captcha.png')
# print("Please solve the captcha manually. Captcha image saved as 'captcha.png'")
# captcha_code = input("Enter Captcha: ")  # Allow user to input captcha
#
# captcha_field.send_keys(captcha_code)

# Submit the form
submit_button = driver.find_element(By.TAG_NAME, 'button')
submit_button.click()

# Wait for the page to load after login
time.sleep(5)  # Adjust the wait time as needed based on the page load time

# Get all the text from the page
page_text = driver.find_element(By.TAG_NAME, "body").text

# Print the text
print(page_text)

# Optionally, save the text to a file
with open("page_text.txt", "w", encoding="utf-8") as f:
    f.write(page_text)

# Close the browser
driver.quit()
