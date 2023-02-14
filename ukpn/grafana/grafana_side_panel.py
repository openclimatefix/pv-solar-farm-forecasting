"""Functions to navigate through the side panel of the dashboard"""
import os
import logging
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
from selenium.webdriver.common.keys import Keys

from ukpn.grafana.grafana_feature_panel import feature_panel

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)

class download_data(feature_panel):
    """Fucntions to download required data"""
    def __init__(
        self,
        download_directory:str = None,
        required_data: str = "Solar") -> None:
        super().__init__()
        self.download_directory = download_directory
        self.required_data = required_data

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
                else:
                    break
            seconds += 1
        return seconds        
    
    def click_on_data_dialog(self):
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
            return None

    def check_required_data_on_top(self):
        """Checking if the required data is on top"""
        try:
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

    def _click_download_button(self):
        """Click the download button"""
        try:
            # Clicking the download button
            xpath = "//button[@class='css-1m1pv8n-button']"
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.element.click()
            return 1
        except NoSuchElementException:
            logger.debug("There is no Download button!")
            logger.debug("Check if the GSP has the required data to download!")
            return None

    def check_and_download_data(
        self):
        """Check if the GSP has required data and download"""
        # Checking if the GSP has solar data
        logger.info(f"Checking if {self.gsp_name} GSP has {self.required_data} data")
        try:
            xpath = "//div[@class=' css-1xwhpd8']"
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except NoSuchElementException:
            logger.debug(f"{self.gsp_name} GSP has no dropdown data panel")
            return None
        else:
            if self.required_data in self.element.text:
                # Input the required data (Solar)
                logger.info(f"Inserting the variable '{self.required_data}'")
                xpath = "//input[contains(@id, 'react-select')]"
                self.element = self.driver.find_element(By.XPATH, xpath)  
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))                  
                self.element.send_keys(f"{self.required_data}")
                self.element.send_keys(Keys.RETURN)

                # Clicking the download button
                logger.info("Clicking the 'Download CSV button")
                status = self._click_download_button()
                return status
            else:
                logger.debug(f"{self.gsp_name} GSP does not have {self.required_data} data")
                return None

    def close_browser(self, timeout: int = 20):
        """Refresh the browser after download finish"""
        # Refresh the driver
        logger.info("Waiting for the download to finish!")
        self._wait_for_download_to_finish(timeout=timeout)
        try:
            logger.info("Closing the browser")
            self.driver.close()
        except InvalidSessionIdException:
            logger.debug("Browser session expired!")

