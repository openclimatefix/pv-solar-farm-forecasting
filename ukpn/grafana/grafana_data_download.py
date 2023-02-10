"""Automate the download of the Grafana data"""
import os
from typing import Optional
from time import sleep
import logging
from typing import List

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, 
    TimeoutException, 
    ElementClickInterceptedException,
    InvalidSessionIdException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


logger_webdriver = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger_webdriver.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format = '%(asctime)s : %(levelname)s : %(message)s ')
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
        self.download_directory = download_directory
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
    
    def wait_for_download_to_finish(
        self,
        timeout: int):
        """ Wait for downloads to finish with a specified timeout.

        Args
        ----
        directory : str
            The path to the folder where the files will be downloaded.
        timeout : int
            How many seconds to wait until timing out.
        """
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            sleep(1)
            dl_wait = False
            files = os.listdir(self.download_directory)
            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 1
        return seconds

    def Initialise_chrome(
        self,
        refresh_window: Optional[bool] = False)-> None:
        """Initalise the chrome browser""" 
        try:
            # Download the browser            
            logger.info(f"Driver is getting downloaded")            
            self.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = self.opts)

            # Open the link in a tab
            self.driver.get(self.url_link)
            self.driver.implicitly_wait(15)
            self.driver.maximize_window()

            # Setting up a wait period of 30 seconds for browser operations 
            self.wait = WebDriverWait(self.driver, 30)

            # Checking the website load status
            title = self.driver.title
            if title is not None:
                logger.info("Webpage successfully loaded")
                logger.info(f"The title of webpage is {title}")
        
        except TimeoutException:
            logger.debug("Page load timeout occured!")
            logger.debug("Check the url link!")
            self.driver.refresh()
        
        else:
            # Option to refresh the browser
            if refresh_window:
                self.driver.refresh()
                logger.info("Browser window refreshed!")


    def get_gsp_names_from_dashbaord(self) -> List:
        """Function to get all the GSP names"""
        # Clicking the dialog box of gsp name
        logger.info("Getting the GSP names from the dashboard")
        gsp_names = []

        try:
            self.element = self.driver.find_element(
                By.XPATH, "//a[@class = 'css-10l6kcd']")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='css-10l6kcd']")))
            self.element.click()
        
        except NoSuchElementException:
            logger.debug("Check the link")
            logger.debug("Increase browser loading wait time!")
            self.driver.close()
        else:
            # Finding the drop down of GSP names
            self.elements = self.driver.find_elements(
                By.XPATH, "//span[contains(@aria-label, 'Dashboard template variables')]")
            self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//span[contains(@aria-label, 'Dashboard template variables')]")))
            
            # Getting each gsp name
            for element in self.elements:
                gsp_names.append(element.text)
            
            # Refreshing the browser
            logger.info("Closing the browser")
            self.driver.close()

        return gsp_names

    def set_gsp_name_in_dashboard(
        self,
        gsp_name: str)-> None:
        """Set the GSP name in the dashboard
        Args:
            gsp_name: Should be All caps, and reflects sytnax from dashboard names
        """
        # Declaring the GSP name
        self.gsp_name = gsp_name
        try:
            # Clicking on the gsp name dialog box to input required gsp name            
            logger.info("Clicking on the GSP dialog box")
            self.element = self.driver.find_element(By.XPATH, "//a[@class = 'css-10l6kcd']")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class = 'css-10l6kcd']")))
            self.element.click()

        except ElementClickInterceptedException:
            logger.debug(f"The dialog box is open to enter a {self.gsp_name} GSP")
            pass
        
        else:
            # Selecting from the drop down
            logger.info("Searching for the dropdown of GSP names")
            self.elements = self.driver.find_elements(By.XPATH, "//div[@class='variable-options-column']")
            self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='variable-options-column']")))
            
            # Inserting the gsp name in the dashboard
            try:
                logger.info(f"Selecting the {self.gsp_name} GSP")
                self.element = self.driver.find_element(
                    By.XPATH, f"//a[@class='variable-option pointer']//span[text()='{self.gsp_name}']")
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//a[@class='variable-option pointer']//span[text()='{self.gsp_name}']")))
                self.element.click()

            except NoSuchElementException:
                logger.info(f"Selecting the {self.gsp_name} GSP")
                self.element = self.driver.find_element(
                    By.XPATH, f"//a[@class='variable-option pointer selected']//span[text()='{self.gsp_name}']"
                    )
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//a[@class='variable-option pointer selected']//span[text()='{self.gsp_name}']")))
                self.element.click()

    def scroll_to_element_and_click(
        self,
        element_id: str = "panel-42",
        panel_title_class:str = "panel-title-text",
        panel_title_text: str = "Generator outputs for all metered generation",     
        drop_down_class:str = "dropdown-item-text",
        drop_down_text:str = "Inspect")-> None:
        """Scroll to the element needed"""
        try:
            # Scrolling to the element        
            logger.info(f"Seaching for the '{panel_title_text}' panel of {self.gsp_name}")
            self.element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
            
            # Clicking on the panel
            logger.info(f"Clicking on the '{panel_title_text}' panel of {self.gsp_name}")
            self.element = self.driver.find_element(By.XPATH, f"//span[@class='{panel_title_class}' and text()='{panel_title_text}']")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='{panel_title_class}' and text()='{panel_title_text}']")))
            self.element.click()

            # Get the side inspect element
            logger.info(f"CLicking on the {drop_down_text} element of {self.gsp_name}")
            self.element = self.driver.find_element(By.XPATH, f"//span[@class='{drop_down_class}' and text()='{drop_down_text}']")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='{drop_down_class}' and text()='{drop_down_text}']")))
            self.element.click()
        
        except NoSuchElementException or TimeoutException:
            logger.debug("Check the url link!")
            logger.debug("Increase the page loading wait time!")
            logger.info("Closing the browser")
            self.driver.close()

    def download_from_side_panel(
        self,
        timeout: int = 20,
        required_data: str = "Solar",
        close_browser: Optional[bool] = False):
        """Download the csv file from the side panel"""

        try:
            # Clicking on the Dataoptions
            logger.info("Searching for 'DataOptions' element in the side panel")
            self.element = self.driver.find_element(By.XPATH, "//div[@class='css-dridf8']")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='css-dridf8']")))
            self.element.click()

        except NoSuchElementException:
            logger.debug("There is no data to be downloaded on the side panel")
            logger.info("Closing the browser")
            self.driver.close()
            return None
        
        else:
            # checking if GSP has the required data (Solar)
            self.element = self.driver.find_element(By.XPATH, "//div[@class='css-1h5d4ck']").get_attribute("title")
            if not self.element == required_data:
                try:
                    # Clicking the dialog box to enter the term (Solar)
                    logger.info("Clicking on the dialog box of type of data")
                    logger.info("Type of data are Solar, Wind, Diesel, etc.")
                    self.element = self.driver.find_element(By.XPATH,"//div[@class='css-17rc2pp-input-wrapper']")
                    self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='css-17rc2pp-input-wrapper']")))
                    self.element.click()
                
                except NoSuchElementException:
                    logger.debug(f"{self.gsp_name} GSP does not have {required_data} data")
                    logger.info("Closing the browser")
                    self.driver.close()
                    return None
                
                else:
                    # Checking if the GSP has solar data
                    logger.info(f"Checking if {self.gsp_name} GSP has {required_data} data")
                    self.element = self.driver.find_element(By.XPATH, "//div[@class=' css-1xwhpd8']")
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class=' css-1xwhpd8']")))

                    if required_data in self.element.text:
                        # Input the required data (Solar)
                        logger.info(f"Inserting the variable '{required_data}'")
                        self.element = self.driver.find_element(By.ID, "react-select-3-input")
                        self.element.send_keys(f"{required_data}")
                        self.element.send_keys(Keys.RETURN)

                        # Clicking the download button
                        logger.info("Clicking the 'Download CSV button")
                        self.element = self.driver.find_element(By.XPATH, "//button[@class='css-1m1pv8n-button']")
                        self.element.click()
                    else:
                         logger.debug(f"{self.gsp_name} GSP does not have {required_data} data")
                         logger.info("Closing the browser")
                         self.driver.close()
                         return None           
            
            else:
                # Finding and clicking download csv 
                logger.info(f"{self.gsp_name} has {required_data} on top")
                self.element = self.driver.find_element(By.XPATH, "//button[@class='css-1m1pv8n-button']")
                self.element.click()

            if close_browser:
                # Close the driver
                self.wait_for_download_to_finish(timeout = timeout)
                logger.info("Closing the browser")
                try:
                    self.driver.close()
                except InvalidSessionIdException:
                    pass
        logger.info("If the download is successful, returns int(1)")
        return 1