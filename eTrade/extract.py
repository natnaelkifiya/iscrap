from selenium.webdriver.common.by import By
import time

class Clicker:
    def __init__(self, driver):
        # Store the driver instance passed to this class
        self.driver = driver

    def click_button(self):
        try:
            # Locate the submit button with text "ፈልግ" and click i
            # Wait for the table to load (you may need to adjust the waiting mechanism)
            driver.implicitly_wait(10)


            myButton = "//table//button"

            # Locate the table (you can refine this by adding more specific attributes if needed)
            buttonClick = driver.find_element(By.XPATH,myButton)

            # Locate the button inside the table, specifically within a particular row
            # Since you provided the full table, let's target the first button in the table
            # button = table.find_element(By.XPATH, '//tr[@role="row"]//button')

            # Click the button
            buttonClick.click()


            driver.implicitly_wait(10)

            # Optional: Extract the page source after the button click
            # page_html = driver.page_source
         
            # print(page_html)

            # time.sleep(100)

        except Exception as e:
            print(f"An error occurred: Extract {e}")
