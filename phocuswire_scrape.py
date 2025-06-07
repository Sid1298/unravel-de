# import requests
# URL = "https://www.phocuswire.com/Latest-News"
# response = requests.get(URL)
# print(response.status_code)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_and_save_html():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://www.phocuswire.com/Latest-News"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(5)  # Wait added for JS to fully load the content
        with open("phocuswire_latest_news.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("HTML content saved to phocuswire_latest_news.html")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_and_save_html()
