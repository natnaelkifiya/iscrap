import os
import json
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

grid_url ='http://172.17.0.2:4444/wd/hub'


# Configure logging
logging.basicConfig(
    filename='etrade_logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Loader:
    def __init__(self, url):
        self.driver = None
        self.url = url

    def load_page(self, tin='0011385997'):
        logging.info(f"Loader initiated with TIN: {tin}")
        print('Loader initiated ...', end='\r')
        
        if not is_online(self.url):
            logging.error(f"Website {self.url} is offline or unreachable.")
            print(f"Website {self.url} is offline or unreachable.", end='/r')
            return None

        # Initialize Firefox WebDriver in headless mode
        service = Service(GeckoDriverManager().install())  # Automatically installs GeckoDriver
        options = Options()
        options.headless = True  # Headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')


        # logging.info("Chrome driver initialized with headless options.")
        

        try:

            # Initialize the WebDriver with the updated method
            self.driver = webdriver.Remote(command_executor=grid_url, options=options)
            # self.driver = webdriver.Chrome(service=service, options=options)
            logging.info(f"Opening URL: {self.url}")
            self.driver.get(self.url)

            # Wait for button to appear and click it
            self.click_button()
            time.sleep(5)  # Give time for the page to load fully
            extract(self.driver)  # Extract data

        except Exception as e:
            print(f"Error occurred while loading page", end='/r')
            logging.error(f"Error occurred while loading page: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                # logging.info("Chrome driver closed.")

    def click_button(self):
        """Clicks the required button on the page if present."""
        try:
            xpath = "//tbody[@class='mdc-data-table__content ng-star-inserted']//tr[@role='row']//button[contains(@class, 'mdc-button--outlined')]"
            button_click = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            button_click.click()
            logging.info("Button clicked successfully.")
        except Exception as e:
            logging.error(f"Button not found or invalid TIN. Error: {e}")
            print(f"Button not found",end='/r')


def is_online(url):
    """Check if the website is reachable."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Website check failed: {e}")
        print('Website ping not responding ...', end='/r')
        return False


def extract(driver):
    """Extracts relevant content from the webpage."""
    data = {}

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//p[text()="አድራሻ"]'))
        )
        
        left_top_panel = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[1]/div/div[1]/div')
        left_bottom_panel = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[1]/div/div[2]')
        main_body_top = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[2]/div/app-business-license/div/div/div[1]')
        main_body_middle = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[2]/div/app-business-license/div/div/div[2]')
        main_body_bottom = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[2]/div/app-business-license/div/div/div[3]/mat-list')

        left_top_div_elements = left_top_panel.find_elements(By.TAG_NAME, 'div')
        left_bottom_div_elements = left_bottom_panel.find_elements(By.TAG_NAME, 'div')
        main_div_top_elements = main_body_top.find_elements(By.TAG_NAME, 'div')
        main_div_middle_elements = main_body_middle.find_elements(By.TAG_NAME, 'div')
        main_div_bottom_elements = main_body_bottom.text.strip()

        data = log_arranger(left_top_div_elements, left_bottom_div_elements, main_div_top_elements, main_div_middle_elements, main_div_bottom_elements)

        log_to_json(data)

    except Exception as e:
        logging.error(f"Error during extraction: {e}")
        print('Could not extract data points ...', end='/r')


def log_arranger(lt, lb, mt, mm, mb):
    """Arrange extracted logs in a specific format."""
    data = {}

    for div in lt:
        try:
            p_element = div.find_element(By.TAG_NAME, 'p')
            span_element = div.find_element(By.TAG_NAME, 'span')
            if p_element and span_element:
                data[p_element.text.strip()] = span_element.text.strip()
        except Exception as e:
            logging.warning(f"Error extracting left top panel: {e}")
            print("Error extracting left top panel:", end='/r')

    for div in lb:
        try:
            span_element = div.find_element(By.TAG_NAME, 'p')
            if span_element:
                data['ስራ አስኪያጅ'] = span_element.text.strip()
        except Exception as e:
            logging.warning(f"Error extracting left bottom panel: {e}")

    for div in mt:
        try:
            p_element = div.find_element(By.TAG_NAME, 'p')
            span_element = div.find_element(By.TAG_NAME, 'span')
            if p_element and span_element:
                data[p_element.text.strip()] = span_element.text.strip()
        except Exception as e:
            logging.warning(f"Error extracting main top panel: {e}")

    for div in mm:
        try:
            p_elements = div.find_elements(By.TAG_NAME, 'p')
            if len(p_elements) >= 2:
                data[p_elements[0].text.strip()] = p_elements[1].text.strip()
        except Exception as e:
            logging.warning(f"Error extracting main middle panel: {e}")

    data['ዘርፎች'] = mb
    return data


def log_to_json(data):
    """Logs the extracted data into a JSON file."""
    try:
        file_path = 'etrade_logs/2024-10.json'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

        with open(file_path, 'r') as f:
            existing_data = json.load(f)

        existing_data.append(data)

        with open(file_path, 'w') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        logging.info("Data successfully logged to JSON.")
    except Exception as e:
        logging.error(f"Issue writing to JSON file: {e}")


if __name__ == "__main__":
    url = "https://etrade.gov.et/business-license-checker?tin=0021385998"
    loader_instance = Loader(url)
    loader_instance.load_page()







# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import requests
# import time

# import os
# import json
# import logging


# class Loader:
#     def __init__(self, url):
#         self.driver = None
#         self.url = url

#     def load_page(self, tin='0011385997'):
#         print("Log: ", "Insider Loader")

#         # Check if the website is online
#         if not is_online(self.url):
#             print(f"Website {self.url} is offline or unreachable.")
#             return None

#         # Setup Chrome WebDriver (Headless Mode)
#         service = Service(ChromeDriverManager().install())
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')  # Headless mode to prevent opening browser windows
#         options.add_argument('--disable-gpu')  # Disable GPU for headless mode
#         options.add_argument('--no-sandbox')  # Bypass OS security model
#         options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

#         print("Log: ", "Driver param set")

#         try:
#             self.driver = webdriver.Chrome(service=service, options=options)
#             print(f"Opening {self.url}")
#             self.driver.get(self.url)  # Load the URL

#             # Wait for button to appear
#             xpath = "//tbody[@class='mdc-data-table__content ng-star-inserted']//tr[@role='row']//button[contains(@class, 'mdc-button--outlined')]"
#             try:
#                 button_click = WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, xpath))
#                 )
#                 button_click.click()  # Click the button
#                 print("Button clicked successfully.")
#             except Exception as e:
#                 print(f'Button not found or invalid TIN. Error: {e}')
#                 return None

#             # Sleep to let page load fully
#             time.sleep(10)

#             # Extract data from the page
#             extract(self.driver)

#         except Exception as e:
#             print(f'Error occurred while loading page: {e}')
#         finally:
#             if self.driver:
#                 self.driver.quit()  # Ensure the driver is closed

# def is_online(url):
#     """Check if the website is reachable."""
#     try:
#         response = requests.get(url, timeout=5)
#         return response.status_code == 200
#     except requests.RequestException:
#         return False
    
# def extract(driver):
#     data = {}
#     """Extract relevant content from the webpage."""
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, '//p[text()="አድራሻ"]'))
#         )

#         left_top_panel = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[1]/div/div[1]/div')
#         left_bottom_panel = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[1]/div/div[2]')
#         main_body_top = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[2]/div/app-business-license/div/div/div[1]')
#         main_body_middle = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[2]/div/app-business-license/div/div/div[2]')
#         main_body_bottom = driver.find_element(By.XPATH, '/html/body/app-root/app-business-license-checker/div/div/div[2]/div[2]/div/app-business-license/div/div/div[3]/mat-list')
        
#         left_top_div_elements = left_top_panel.find_elements(By.TAG_NAME, 'div')
#         left_bottom_div_elements = left_bottom_panel.find_elements(By.TAG_NAME, 'div')
        
#         main_div_top_elements = main_body_top.find_elements(By.TAG_NAME, 'div')
#         main_div_middle_elements = main_body_middle.find_elements(By.TAG_NAME, 'div')

#         main_div_bottom_elements = main_body_bottom.text.strip()

#         try:
#             data =  log_arranger(left_top_div_elements, left_bottom_div_elements, main_div_top_elements, main_div_middle_elements, main_div_bottom_elements)
#         except:
#             print('Error Log: could not extract content.' )
#         try:
#             file_path = 'etrade_logs/2024-10.json'
#             log_to_json(data)

#         except:
#             print('issue writing  to file ')

#     except Exception as e:
#         print(f"Error during extraction: {e}")

        


# def log_to_json(data_dict):
#     try:
#         file_path = 'etrade_logs/2024-10.json'

#         # Ensure the directory exists
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)

#         # Check if the file exists, create if not, and append the data
#         if not os.path.exists(file_path):
#             with open(file_path, 'w') as f:
#                 json.dump([], f)

#         # Read existing data
#         with open(file_path, 'r') as f:
#             existing_data = json.load(f)

#         # Append new data
#         existing_data.append(data_dict)

#         # Write updated data back to the file
#         with open(file_path, 'w') as f:
#             json.dump(existing_data, f, ensure_ascii=False, indent=4)

#     except Exception as e:
#         print('Issue writing to file:', e)  # Print the error message



# def log_arranger(lt, lb, mt, mm, mb):
#     """Arrange extracted logs in a specific format."""
#     data = {}

#     for index, div in enumerate(lt):
#         p_element = div.find_element(By.TAG_NAME, 'p')  # Find the first <p> element
#         span_element = div.find_element(By.TAG_NAME, 'span')  # Find the first <span> element

#         # Extract text from both elements
#         if p_element and span_element:  # Ensure both elements are found
#             key = p_element.text.strip()  # First element as the key
#             value = span_element.text.strip()  # Second element as the value
#             data[key] = value  # Add to the dictionary
#             if 'የተመዘገበበት ቀን' in key:
#                 break  # Exit the loop when 'xyz' is found


#     for index, div in enumerate(lb):  
#         span_element = div.find_element(By.TAG_NAME, 'p')  # Find the first <span> element

#         # Extract text from both elements
#         if span_element:  # Ensure both elements are found
#             key = 'ስራ አስኪያጅ'  # First element as the key
#             value = span_element.text.strip()  # Second element as the value
#             data[key] = value  # Add to the dictionary
   
#     # print(data)

#     for index, div in enumerate(mt):
#         try:

#             p_element = div.find_element(By.TAG_NAME, 'p')  # Find the first <p> element
#             span_element = div.find_element(By.TAG_NAME, 'span')  # Find the first <span> element

#             # Extract text from both elements
#             if p_element and span_element:  # Ensure both elements are found
#                 key = p_element.text.strip()  # First element as the key
#                 value = span_element.text.strip()  # Second element as the value
#                 data[key] = value  # Add to the dictionary
#                 if 'የተመዘገበበት ቀን' in key:
#                     break  # Exit the loop when 'xyz' is found
#         except:
#             print('Error Extracting main body dv')


#     for index, div in enumerate(mm):
#         try:
#             p_elements = div.find_elements(By.TAG_NAME, 'p')

#             # Access the first and second <p> elements
#             p_element = p_elements[0]  # First <p> element
#             span_element = p_elements[1]  # Second <p> element


#             # Extract text from both elements
#             if p_element and span_element:  # Ensure both elements are found
#                 key = p_element.text.strip()  # First element as the key
#                 value = span_element.text.strip()  # Second element as the value
#                 data[key] = value  # Add to the dictionary
#         except:
#             print('Error Extracting main body dv')
#     # print(data)

#     #sector
#     data['ዘርፎች'] = mb


#     return data


#     # sector






# if __name__ == "__main__":
#     # Provide the correct URL here
#     url = "https://etrade.gov.et/business-license-checker?tin=0021385998"
#     loader_instance = Loader(url)
#     loader_instance.load_page()  # Optionally pass a TIN number if needed
