from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options if needed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start browser maximized

# Create an instance of the WebDriver (for Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open a website
driver.get('https://blsitalypakistan.com/')

# Get all the text from the page
page_text = driver.find_element("tag name", "body").text

# Print the text
print(page_text)
print("Scraped Successfully")
# Close the browser
driver.quit()
