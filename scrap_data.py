import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ProductScraper:
    def __init__(self, driver_path, url):
        self.url = url
        self.driver = self._init_driver(driver_path)
        self.product_data = []
        self.page_number = 1

    def _init_driver(self, driver_path):
        # Initializing the Selenium driver with custom options
        service = Service(driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def wait_for_element(self, by, value, timeout=30):
        """ 
        Wait for element in pages to load using a set timeout value.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def scrape_page(self):
        """ 
        Get information from web pages using the tag attributes
        """
        print(f"Scraping page {self.page_number}")
        try:
            self.wait_for_element(By.CLASS_NAME, "produts")
        except TimeoutException:
            print("Timeout waiting for products to load. Moving to next step.")
            return False

        # Find all product elements and extract information
        products = self.driver.find_elements(By.CLASS_NAME, "produts")
        print(f"Products found on page {self.page_number}: {len(products)}")

        for product in products:
            try:
                product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                product_name = product.find_element(By.TAG_NAME, "h2").text.strip()
                product_type = product.find_elements(By.TAG_NAME, "h2")[1].text.strip()
                document_url = product.find_element(By.CLASS_NAME, "p_image").get_attribute("src")

                self.product_data.append({
                    "name": product_name,
                    "category": product_type,
                    "product_url": product_link,
                    "document": document_url
                })
            except Exception as e:
                print(f"Error extracting product data: {e}")
        return True

    def go_to_next_page(self):
        """ 
        function to automatically click the next page. 
        """
        try:
            next_button = self.wait_for_element(
                By.XPATH, "//span[contains(@class, 'next') and contains(@class, 'common_selector_pages')]"
            )
            if next_button and next_button.is_displayed() and next_button.is_enabled():
                print("Found 'Next' button. Clicking...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(0.1)
                self.page_number += 1
                return True
            else:
                print("Next button not clickable. Ending pagination.")
                return False
        except NoSuchElementException:
            print("Next button not found. Ending pagination.")
            return False
        except Exception as e:
            print(f"Error during pagination: {e}")
            return False

    def save_to_json(self, file_name="product_data.json"):
        with open(file_name, "w", encoding='utf-8') as json_file:
            json.dump(self.product_data, json_file, indent=4, ensure_ascii=False)
        print(f"Data saved to {file_name}. Total products scraped: {len(self.product_data)}")

    def run(self):
        self.driver.get(self.url)
        while self.scrape_page():
            if not self.go_to_next_page():
                break
        self.driver.quit()
        self.save_to_json()

# run the script
if __name__ == "__main__":
    scraper = ProductScraper(driver_path='chromedriver.exe', url='https://www.firstplanit.com/site/productlist')
    scraper.run()
