from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_all_cookies_and_csrf(url):
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Create WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Load the page
    driver.get(url)
    time.sleep(5)  # Let JS and DOM load

    # Extract cookies
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

    # Extract page source and parse CSRF token
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    csrf_token = csrf_input['value'] if csrf_input else None

    driver.quit()
    return cookies, csrf_token

# Example usage
url = "https://ebixcash.com/find-our-agents/"
# cookies_dict, csrf_token = get_all_cookies_and_csrf(url)
# print("Cookies:", cookies_dict)
# print("CSRF Token:", csrf_token)
