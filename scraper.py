from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from datetime import datetime

class ElectricityMeterScraper:
    def __init__(self):
        # Get account number from environment variable for security
        self.account_number = os.getenv('ACCOUNT_NUMBER', '37226784')
        self.driver = None
        
        # List of all meter numbers
        self.all_meters = ['37226784', '37202772', '37195501', '37226785', '37202771']
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # Run in headless mode for cloud
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Cloud deployment (Replit) - use system chromedriver
        self.driver = webdriver.Chrome(options=options)
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return True
    
    def debug_page_structure(self):
        try:
            print("\n=== PAGE DEBUG INFO ===")
            print(f"Page Title: {self.driver.title}")
            print(f"Current URL: {self.driver.current_url}")
            
            # Find all input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"\nFound {len(inputs)} input fields:")
            for i, inp in enumerate(inputs):
                try:
                    print(f"  {i+1}. Type: {inp.get_attribute('type')}, "
                          f"Placeholder: {inp.get_attribute('placeholder')}, "
                          f"ID: {inp.get_attribute('id')}, "
                          f"Class: {inp.get_attribute('class')}")
                except:
                    print(f"  {i+1}. Unable to get attributes")
            
            # Find all buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"\nFound {len(buttons)} buttons:")
            for i, btn in enumerate(buttons):
                try:
                    print(f"  {i+1}. Text: '{btn.text}', "
                          f"Type: {btn.get_attribute('type')}, "
                          f"Class: {btn.get_attribute('class')}")
                except:
                    print(f"  {i+1}. Unable to get attributes")
            
            print("=== END DEBUG INFO ===\n")
            
        except Exception as e:
            print(f"Debug failed: {str(e)}")
        
    def login(self, website_url):
        try:
            print("Navigating to website...")
            self.driver.get(website_url)
            time.sleep(5)
            
            # Debug page structure
            self.debug_page_structure()
            
            print("Looking for account input field...")
            account_input = None
            
            # Try multiple selectors for the account input
            selectors = [
                "input[placeholder*='Account']",
                "input[placeholder*='Meter']", 
                "input[type='text']",
                "#uid-t2vzsdhxgh",
                "input.form-control"
            ]
            
            for selector in selectors:
                try:
                    account_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found input field with selector: {selector}")
                    break
                except:
                    continue
            
            if not account_input:
                print("Trying to find any input field...")
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if inputs:
                    account_input = inputs[0]
                    print(f"Using first input field found")
                else:
                    raise Exception("No input field found on the page")
            
            print(f"Entering account number: {self.account_number}")
            account_input.clear()
            account_input.send_keys(self.account_number)
            time.sleep(2)
            
            print("Looking for login button...")
            login_button = None
            
            # Try multiple selectors for the login button
            button_selectors = [
                "button.btn-primary",
                "button[type='button']",
                "button.btn",
                "button",
                "input[type='submit']"
            ]
            
            for selector in button_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if any(text in btn.text.lower() for text in ['login', 'submit', 'enter']):
                            login_button = btn
                            print(f"Found login button with text: {btn.text}")
                            break
                    if login_button:
                        break
                except:
                    continue
            
            if not login_button:
                print("Trying to find any button...")
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    login_button = buttons[0]
                    print(f"Using first button found: {login_button.text}")
                else:
                    raise Exception("No login button found on the page")
            
            print("Clicking login button...")
            self.driver.execute_script("arguments[0].click();", login_button)
            time.sleep(5)
            
            print("Login attempt completed")
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            print("Current page title:", self.driver.title)
            print("Current URL:", self.driver.current_url)
            return False
    
    def debug_logged_in_page(self):
        try:
            print("\n=== LOGGED-IN PAGE DEBUG ===")
            print(f"Page Title: {self.driver.title}")
            print(f"Current URL: {self.driver.current_url}")
            
            # Find all spans with data-v attributes (likely Vue.js components)
            spans = self.driver.find_elements(By.TAG_NAME, "span")
            print(f"\nFound {len(spans)} span elements:")
            
            for i, span in enumerate(spans):
                try:
                    text = span.text.strip()
                    if text and len(text) > 0:
                        attrs = span.get_attribute("outerHTML")[:100]
                        print(f"  {i+1}. Text: '{text}' | HTML: {attrs}...")
                except:
                    continue
            
            # Also check divs with data
            divs = self.driver.find_elements(By.TAG_NAME, "div")
            print(f"\nChecking {len(divs)} div elements for data:")
            
            for i, div in enumerate(divs):
                try:
                    text = div.text.strip()
                    if text and ("BDT" in text or any(month in text for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])):
                        attrs = div.get_attribute("outerHTML")[:150]
                        print(f"  DIV {i+1}. Text: '{text}' | HTML: {attrs}...")
                except:
                    continue
            
            print("=== END LOGGED-IN DEBUG ===\n")
            
        except Exception as e:
            print(f"Logged-in page debug failed: {str(e)}")

    def extract_numeric_balance(self, balance_text):
        """Extract numeric balance value from balance text"""
        try:
            if not balance_text or balance_text in ['Not found', 'Error']:
                return None
            
            # Extract numbers from the balance text
            import re
            numbers = re.findall(r'[\d,]+\.?\d*', balance_text)
            
            for number in numbers:
                try:
                    # Clean and convert to float
                    clean_number = number.replace(',', '')
                    balance_value = float(clean_number)
                    
                    # Only consider reasonable balance values (between 0 and 10000)
                    if 0 <= balance_value <= 10000:
                        return balance_value
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"Error extracting numeric balance: {str(e)}")
            return None

    def extract_data(self):
        try:
            print("Waiting for page to load after login...")
            time.sleep(5)
            
            # Debug the logged-in page structure
            self.debug_logged_in_page()
            
            data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "account_number": self.account_number,
                "status": "success"
            }
            
            # Wait for any data elements to load
            time.sleep(3)
            
            # Get all text elements on the page
            all_elements = self.driver.find_elements(By.XPATH, "//*[text()]")
            all_texts = []
            
            for element in all_elements:
                try:
                    text = element.text.strip()
                    if text and len(text) > 0:
                        all_texts.append(text)
                except:
                    continue
            
            print(f"Found {len(all_texts)} text elements")
            
            # Extract remaining balance (look for balance-related patterns)
            try:
                balance_found = False
                for text in all_texts:
                    # Look for current balance, remaining balance, etc.
                    if ("balance" in text.lower() or "remaining" in text.lower()) and "BDT" in text:
                        data["remaining_balance"] = text
                        print(f"Found remaining balance: {text}")
                        balance_found = True
                        break
                
                if not balance_found:
                    # Look for any BDT amount that might be the balance
                    for text in all_texts:
                        if "BDT" in text and any(char.isdigit() for char in text):
                            # Skip if it looks like the recharge amount (3,000.00)
                            if "3,000" not in text and "3000" not in text:
                                data["remaining_balance"] = text
                                print(f"Found potential balance: {text}")
                                break
                    else:
                        data["remaining_balance"] = "Not found"
                        print("Remaining balance not found")
                
                # Extract numeric balance for comparison
                data["balance_numeric"] = self.extract_numeric_balance(data.get("remaining_balance"))
            except Exception as e:
                data["remaining_balance"] = "Error"
                print(f"Error extracting balance: {str(e)}")
            
            # Extract reading time (look for dates that might be meter reading)
            try:
                reading_found = False
                for text in all_texts:
                    if ("reading" in text.lower() or "meter" in text.lower()) and any(month in text for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                        data["reading_time"] = text
                        print(f"Found reading time: {text}")
                        reading_found = True
                        break
                
                if not reading_found:
                    # Look for any date that's not the recharge date (not July 10)
                    for text in all_texts:
                        if any(month in text for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) and ":" in text:
                            if "10 Jul" not in text:  # Skip the recharge date
                                data["reading_time"] = text
                                print(f"Found potential reading time: {text}")
                                break
                    else:
                        data["reading_time"] = "Not found"
                        print("Reading time not found")
            except Exception as e:
                data["reading_time"] = "Error"
                print(f"Error extracting reading time: {str(e)}")
            
            # Extract last recharge amount (specifically look for 3,000.00 BDT)
            try:
                for text in all_texts:
                    if "3,000" in text and "BDT" in text:
                        data["last_recharge_amount"] = text
                        print(f"Found recharge amount: {text}")
                        break
                else:
                    data["last_recharge_amount"] = "Not found"
                    print("Recharge amount not found")
            except Exception as e:
                data["last_recharge_amount"] = "Error"
                print(f"Error extracting recharge amount: {str(e)}")
            
            # Extract last recharge date (specifically look for 10 Jul 2025)
            try:
                for text in all_texts:
                    if "10 Jul" in text and "2025" in text:
                        data["last_recharge_date"] = text
                        print(f"Found recharge date: {text}")
                        break
                else:
                    data["last_recharge_date"] = "Not found"
                    print("Recharge date not found")
            except Exception as e:
                data["last_recharge_date"] = "Error"
                print(f"Error extracting recharge date: {str(e)}")
            
            return data
            
        except Exception as e:
            print(f"Data extraction failed: {str(e)}")
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "account_number": self.account_number,
                "status": "error",
                "remaining_balance": "Error",
                "reading_time": "Error",
                "last_recharge_amount": "Error",
                "last_recharge_date": "Error",
                "error_message": str(e)
            }
    
    def scrape_account(self, account_number, website_url):
        """Scrape data for a specific account number"""
        try:
            print(f"\n=== Scraping Account: {account_number} ===")
            
            # Set the account number for this scrape
            original_account = self.account_number
            self.account_number = account_number
            
            if not self.setup_driver():
                self.account_number = original_account
                return None
            
            if not self.login(website_url):
                self.account_number = original_account
                return None
            
            time.sleep(2)
            data = self.extract_data()
            
            # Restore original account number
            self.account_number = original_account
            
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            return data
                
        except Exception as e:
            print(f"Scraping failed for account {account_number}: {str(e)}")
            self.account_number = original_account
            if self.driver:
                self.driver.quit()
                self.driver = None
            return None
    
    def scrape_all_meters(self, website_url):
        """Scrape all meters and return list of low balance warnings"""
        low_balance_warnings = []
        all_data = []
        
        for account_number in self.all_meters:
            data = self.scrape_account(account_number, website_url)
            
            if data and data.get('status') == 'success':
                all_data.append(data)
                
                # Check if balance is low (less than 100 BDT)
                balance_numeric = data.get('balance_numeric')
                if balance_numeric is not None and balance_numeric < 100:
                    warning = {
                        'account_number': account_number,
                        'balance_text': data.get('remaining_balance', 'N/A'),
                        'balance_numeric': balance_numeric,
                        'timestamp': data.get('timestamp')
                    }
                    low_balance_warnings.append(warning)
                    print(f"⚠️ LOW BALANCE WARNING: Account {account_number} has {balance_numeric} BDT")
                else:
                    print(f"✅ Account {account_number} has sufficient balance: {balance_numeric} BDT")
            else:
                print(f"❌ Failed to scrape account {account_number}")
            
            # Small delay between accounts
            time.sleep(2)
        
        return low_balance_warnings, all_data
    
    def save_data(self, data):
        try:
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
            print("Data saved successfully")
            return True
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
            return False
    
    def scrape(self, website_url):
        try:
            if not self.setup_driver():
                return False
            
            if not self.login(website_url):
                return False
            
            time.sleep(2)
            data = self.extract_data()
            
            if data:
                self.save_data(data)
                print("Scraping completed successfully!")
                print(f"Remaining Balance: {data.get('remaining_balance', 'N/A')}")
                print(f"Reading Time: {data.get('reading_time', 'N/A')}")
                return True
            else:
                print("Failed to extract data")
                return False
                
        except Exception as e:
            print(f"Scraping failed: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = ElectricityMeterScraper()
    website_url = os.getenv('METER_WEBSITE_URL', 'https://prepaid.desco.org.bd/customer/#/customer-login')
    print(f"Using website URL: {website_url}")
    scraper.scrape(website_url)