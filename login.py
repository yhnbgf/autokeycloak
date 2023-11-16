from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Replace 'path/to/chromedriver' with the actual path to your chromedriver executable
chromedriver_path = '/usr/bin/chromedriver'

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')  # Required for running in a virtual machine
chrome_options.add_argument('--disable-gpu')  # Required for running in a virtual machine
# chrome_options.add_argument('--headless')  # Optional: run in headless mode without a graphical user interface

# Create a Chrome web driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Prompt the user for the website URL
    url = input("Enter the website URL: ")
    driver.get(url)
    time.sleep(5)

    # Read the cookie value from the file
    with open('cookie.txt', 'r') as file:
        keycloak_identity_legacy = file.read().strip()

    # Provided cookie information
    cookie_info = f"document.cookie = 'KEYCLOAK_IDENTITY_LEGACY={keycloak_identity_legacy}';"

    # Execute JavaScript to set the cookie
    driver.execute_script(cookie_info)
    driver.refresh()

    # Optional: Print the title of the webpage
    print("Title of the page:", driver.title)

    # Keep the browser window open until Ctrl+C is pressed
    while True:
        pass

except KeyboardInterrupt:
    # Ctrl+C was pressed, close the browser window
    driver.quit()
