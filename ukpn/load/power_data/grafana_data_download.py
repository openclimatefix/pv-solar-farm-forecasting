"""Automate the download of the Grafana data"""
import os
from typing import Optional
from time import sleep
import logging
import difflib

from typing import List
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

logger = logging.getLogger(__name__)

def get_chrome():
    if os.path.isfile('/usr/bin/chromium-browser'):
        return '/usr/bin/chromium-browser'
    elif os.path.isfile('/usr/bin/chromium'):
        return '/usr/bin/chromium'
    elif os.path.isfile('/usr/bin/chrome'):
        return '/usr/bin/chrome'
    elif os.path.isfile('/usr/bin/google-chrome'):
        return '/usr/bin/google-chrome'
    else:
        return None
class automate_csv_download:
    def __init__(
        self,
        download_directory: str = None,
        url_link: str = "https://dsodashboard.ukpowernetworks.co.uk"
        )-> None:
        """Function to set the desired chrome options"""
        self.url_link = url_link

        self.prefs = {"download.default_directory" : f"{download_directory}"}
        self.opts = Options()
        self.opts.add_experimental_option('prefs', self.prefs)
        self.opts.add_experimental_option("detach", True)
        self.opts.binary_location = get_chrome()
        self.opts.add_argument("--start-maximized")
        self.opts.add_argument('--headless')
        self.opts.add_argument('--no-sandbox')
        self.opts.add_argument('--disable-dev-shm-usage')

    def Initialise_chrome(
        self,
        refresh_window: Optional[bool] = False)-> None:
        """Initalise the chrome browser""" 
        # Download the browser
        self.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = self.opts)

        # Open the link in a tab
        self.driver.get(self.url_link)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

        # Setting up a wait period of 30 seconds for browser operations 
        self.wait = WebDriverWait(self.driver, 30)

        # Option to refresh the browser
        if refresh_window:
            self.driver.refresh()

    def select_gsp_names_by_index(self)-> None:
        """Selecting the gsps by index"""
        # Clicking the dialog box of gsp name
        self.element = self.driver.find_element(By.XPATH, "//a[@class = 'css-10l6kcd']").click()
        # Counting the dropdown elements
        self.elements = self.driver.find_elements(By.XPATH, "//div[@class='variable-options-column']")
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='variable-options-column']")))

    def get_gsp_names_from_dashbaord(self) -> List:
        """Function to get all the GSP names"""
        # Clicking the dialog box of gsp name
        gsp_names = []
        self.element = self.driver.find_element(By.XPATH, "//a[@class = 'css-10l6kcd']").click()

        # Finding the drop down of GSP names
        self.elements = self.driver.find_elements(By.XPATH, "//span[contains(@aria-label, 'Dashboard template variables')]")
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@aria-label, 'Dashboard template variables')]")))
        
        # Getting each gsp name
        for element in self.elements:
            gsp_names.append(element.text)
        
        # Refreshing the browser
        self.driver.refresh()

        return gsp_names

    def set_gsp_name_in_dashboard(
        self,
        gsp_name: str)-> None:
        """Set the GSP name in the dashboard
        Args:
            gsp_name: Should be All caps, and reflects sytnax from dashboard names
        """
        # Clicking on the gsp name dialog box to input required gsp name
        self.search = self.driver.find_element(By.XPATH, "//a[@class = 'css-10l6kcd']").click()

        # Inserting the gsp name
        self.search = self.driver.find_element(By.XPATH, "//input[@class='gf-form-input']")

        # Selecting from the drop down
        self.elements = self.driver.find_elements(By.XPATH, "//div[@class='variable-options-column']")
        self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='variable-options-column']")))
        
        # Inserting the gsp name in the dashboard
        try:
            self.element = self.driver.find_element(
                By.XPATH, f"//a[@class='variable-option pointer']//span[text()='{gsp_name}']")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//a[@class='variable-option pointer']//span[text()='{gsp_name}']")))
            self.element.click()

        except NoSuchElementException:
            self.element = self.driver.find_element(
                By.XPATH, f"//a[@class='variable-option pointer selected']//span[text()='{gsp_name}']"
                )
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//a[@class='variable-option pointer selected']//span[text()='{gsp_name}']")))
            self.element.click()
        
        # # Checking the gsp name
        # self.gsp_name = gsp_name
        # if not len(self.gsp_name.split()) > 1:
        #     self.search.send_keys(gsp_name)
        #     self.search.send_keys(Keys.RETURN)
        #     sleep(5)
        # else:
        #     return None
    
    def scroll_to_element_and_click(
        self,
        element_id: str = "panel-42",
        panel_title_class:str = "panel-title-text",
        panel_title_text: str = "Generator outputs for all metered generation",     
        drop_down_class:str = "dropdown-item-text",
        drop_down_text:str = "Inspect")-> None:
        """Scroll to the element needed"""

        # Scrolling to the element
        self.element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        
        # Clicking on the panel
        self.element = self.driver.find_element(By.XPATH, f"//span[@class='{panel_title_class}' and text()='{panel_title_text}']")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='{panel_title_class}' and text()='{panel_title_text}']")))
        self.element.click()

        # Get the side inspect element
        self.element = self.driver.find_element(By.XPATH, f"//span[@class='{drop_down_class}' and text()='{drop_down_text}']")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='{drop_down_class}' and text()='{drop_down_text}']")))
        self.element.click()

    def download_from_side_panel(
        self,
        required_data: str = "Solar",
        close_browser: Optional[bool] = False)-> None:
        """Download the csv file from the side panel"""

        try:
            # Clicking on the Dataoptions
            self.element = self.driver.find_element(By.XPATH, "//div[@class='css-dridf8']")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='css-dridf8']")))
            self.element.click()
        except NoSuchElementException:
            logger.info("There is no data to be downloaded")
            print("There is no data to be downloaded")
            return None
        
        else:
            # checking if GSP has the required data (Solar)
            self.element = self.driver.find_element(By.XPATH, "//div[@class='css-1h5d4ck']").get_attribute("title")
            if not self.element == required_data:
                # Clicking the dialog box to enter the term (Solar)
                self.element = self.driver.find_element(By.XPATH,"//div[@class='css-17rc2pp-input-wrapper']")
                self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='css-17rc2pp-input-wrapper']")))
                self.element.click()

                # Input the required data (Solar)
                self.element = self.driver.find_element(By.ID, "react-select-3-input")
                self.element.send_keys(f"{required_data}")
                self.element.send_keys(Keys.RETURN)

                # Clicking the download button
                self.element = self.driver.find_element(By.XPATH, "//button[@class='css-1m1pv8n-button']")
                self.element.click()                
            else:
                # Finding and clicking download csv 
                self.element = self.driver.find_element(By.XPATH, "//button[@class='css-1m1pv8n-button']")
                self.element.click()

            if close_browser:
                # Close the driver
                self.driver.close()            

if __name__ == "__main__":
    download_directory = "/home/vardh/ocf/pv-solar-farm-forecasting/tests/data"
    gsp_name = "RAYLEIGH"
    grafana = automate_csv_download(
        download_directory = download_directory
        )
    grafana.Initialise_chrome()
    grafana.set_gsp_name_in_dashboard(gsp_name = gsp_name)
    grafana.scroll_to_element_and_click()
    grafana.download_from_side_panel()
