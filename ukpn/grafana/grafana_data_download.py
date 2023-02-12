"""Automate the download of the Grafana data"""
import logging
import os
from time import sleep
from typing import List, Optional

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidSessionIdException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger_webdriver = logging.getLogger("selenium.webdriver.remote.remote_connection")
logger_webdriver.setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)


def get_chrome():
    """Search for the Chrome driver 'folder'"""
    if os.path.isfile("/usr/bin/chromium-browser"):
        return "/usr/bin/chromium-browser"
    elif os.path.isfile("/usr/bin/chromium"):
        return "/usr/bin/chromium"
    elif os.path.isfile("/usr/bin/chrome"):
        return "/usr/bin/chrome"
    elif os.path.isfile("/usr/bin/google-chrome"):
        return "/usr/bin/google-chrome"
    else:
        return None


class automate_csv_download:
    """Functions to navigate through the UKPN dashboard using Selenium webdriver"""

    def __init__(
        self,
        download_directory: str = None,
        url_link: str = "https://dsodashboard.ukpowernetworks.co.uk",
    ) -> None:
        """Function to set the desired chrome options"""
        self.download_directory = download_directory
        self.url_link = url_link

        self.prefs = {
            "download.default_directory": f"{download_directory}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        }
        self.opts = Options()
        self.opts.add_experimental_option("prefs", self.prefs)
        self.opts.add_experimental_option("detach", True)
        self.opts.binary_location = get_chrome()
        self.opts.add_argument("--start-maximized")
        self.opts.add_argument("--headless")
        self.opts.add_argument("--no-sandbox")
        self.opts.add_argument("--disable-dev-shm-usage")

    def _wait_for_download_to_finish(self, timeout: int):
        """Wait for downloads to finish with a specified timeout.

        Args:
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
                if fname.endswith(".crdownload"):
                    dl_wait = True

            seconds += 1
        return seconds

    def _close_browser(self, timeout: int = 20):
        """Close the browser after download finish"""
        # Close the driver
        self._wait_for_download_to_finish(timeout=timeout)
        logger.info("Closing the browser")
        try:
            self.driver.close()
        except InvalidSessionIdException:
            logger.debug("The driver is already closed!")

    def Initialise_chrome(self, refresh_window: Optional[bool] = False) -> None:
        """Initalise the chrome browser"""
        try:
            # Download the browser
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=self.opts
            )
            logger.info("Driver is getting downloaded")

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
            xpath = "//a[@class = 'css-10l6kcd']"
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()

        except NoSuchElementException:
            logger.debug("Check the link")
            logger.debug("Increase browser loading wait time!")
            self.driver.close()
        else:
            # Finding the drop down of GSP names
            xpath = "//span[contains(@aria-label, 'Dashboard template variables')]"
            self.elements = self.driver.find_elements(By.XPATH, xpath)
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

            # Getting each gsp name
            for element in self.elements:
                gsp_names.append(element.text)

            # Refreshing the browser
            logger.info("Closing the browser")
            self.driver.close()

        return gsp_names

    def click_on_gsp_box(self):
        """Function to click on the GSP dialog box"""
        try:
            # Clicking on the gsp name dialog box to input required gsp name
            xpath = "//a[@class = 'css-10l6kcd']"
            logger.info("Clicking on the GSP dialog box")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return 1

        except ElementClickInterceptedException:
            logger.debug("The dialog box is open to enter a GSP name")
            return None

    def search_for_dropdown(self) -> None:
        """Search for dropdown of GSP names"""
        try:
            # Selecting from the drop down
            xpath = "//div[@class='variable-options-column']"
            logger.info("Searching for the dropdown of GSP names")
            self.elements = self.driver.find_elements(By.XPATH, xpath)
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return 1

        except NoSuchElementException:
            logger.debug("The drop down of gsp names has not been found!")
            return None

    def select_a_gsp(self, gsp_name: str):
        """Select a GSP for the data download"""
        # Inserting the gsp name in the dashboard
        # Declaring the GSP name
        self.gsp_name = gsp_name
        try:
            xpath = f"//a[@class='variable-option pointer']//span[text()='{self.gsp_name}']"
            logger.info(f"Selecting the {self.gsp_name} GSP")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return 1

        except NoSuchElementException:
            logger.info(f"Selecting the {self.gsp_name} GSP")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return None

    def scroll_to_element_and_click(
        self,
        element_id: str = "panel-42",
        panel_title_class: str = "panel-title-text",
        panel_title_text: str = "Generator outputs for all metered generation",
        drop_down_class: str = "dropdown-item-text",
        drop_down_text: str = "Inspect",
    ):
        """Scroll to the element needed"""
        try:
            # Scrolling to the element
            logger.info(f"Seaching for the '{panel_title_text}' panel of {self.gsp_name}")
            self.element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)

            # Clicking on the panel
            xpath = f"//span[@class='{panel_title_class}' and text()='{panel_title_text}']"
            logger.info(f"Clicking on the '{panel_title_text}' panel of {self.gsp_name}")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()

            # Get the side inspect element
            xpath = f"//span[@class='{drop_down_class}' and text()='{drop_down_text}']"
            logger.info(f"CLicking on the {drop_down_text} element of {self.gsp_name}")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return 1

        except NoSuchElementException or TimeoutException:
            logger.debug("Check the url link!")
            logger.debug("Increase the page loading wait time!")
            logger.info("Closing the browser")
            self.driver.close()
            return None

    def click_dataoptions_side_panel(self):
        """Click on the Dataoptions from side panel"""
        try:
            # Clicking on the Dataoptions
            xpath = "//div[@class='css-dridf8']"
            logger.info("Searching for 'DataOptions' element in the side panel")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return 1

        except NoSuchElementException:
            logger.debug("There is no data to be downloaded on the side panel")
            logger.info("Closing the browser")
            self.driver.close()
            return None

    def _click_on_data_dialog(self):
        """Clicking on the data dialog box"""
        try:
            # Clicking the dialog box to enter the term (Solar)
            logger.info("Clicking on the dialog box of type of data")
            logger.info("Type of data are Solar, Wind, Diesel, etc.")
            xpath = "//div[@class='css-17rc2pp-input-wrapper']"
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return 1

        except NoSuchElementException:
            logger.debug(f"This {self.gsp_name} GSP does not have any data")
            logger.info("Closing the browser")
            self.driver.close()
            return None

    def _click_download_button(self) -> None:
        """Click the download button"""
        # Clicking the download button
        logger.info("Clicking the 'Download CSV button")
        xpath = "//button[@class='css-1m1pv8n-button']"
        self.element = self.driver.find_element(By.XPATH, xpath)
        self.element.click()

    def check_required_data_on_top(self, required_data: str = "Solar"):
        """Checking if the required data is on top"""
        try:
            self.required_data = required_data
            # checking if GSP has the required data (Solar)
            xpath = "//div[@class='css-1h5d4ck']"
            self.element = self.driver.find_element(By.XPATH, xpath).get_attribute("title")
            if self.element == self.required_data:
                return 1
            else:
                return None
        except NoSuchElementException:
            logger.debug("No element to click is found")
            return None

    def check_and_download_data(self, required_data: str = "Solar"):
        """Check if the GSP has required data and download"""
        # Checking if the GSP has solar data
        self.required_data = required_data
        logger.info(f"Checking if {self.gsp_name} GSP has {self.required_data} data")
        xpath = "//div[@class=' css-1xwhpd8']"
        self.element = self.driver.find_element(By.XPATH, xpath)
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        if self.required_data in self.element.text:
            # Input the required data (Solar)
            logger.info(f"Inserting the variable '{required_data}'")
            self.element = self.driver.find_element(By.ID, "react-select-3-input")
            self.element.send_keys(f"{required_data}")
            self.element.send_keys(Keys.RETURN)

            # Clicking the download button
            logger.info("Clicking the 'Download CSV button")
            self._click_download_button()
            self._close_browser()
            return 1
        else:
            logger.debug(f"{self.gsp_name} GSP does not have {required_data} data")
            return None
