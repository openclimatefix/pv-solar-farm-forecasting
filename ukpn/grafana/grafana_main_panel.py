"""Functions to Webscrap in the UKPN DSO dashboard main panel"""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException)

from ukpn.grafana.chrome import open_webpage

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)

class main_panel(open_webpage):
    """Functions to navigate through the main panel"""
    def __init__(self) -> None:
        super().__init__()       

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
        
    def select_a_gsp(self, gsp_name:str):
        """Select a GSP for the data download"""
        # Inserting the gsp name in the dashboard
        # Declaring the GSP name
        self.gsp_name = gsp_name 
        try:
            xpath = (
                f"//a[@class='variable-option pointer selected']//span[text()='{self.gsp_name}']"
            )
            logger.info(f"Selecting the {self.gsp_name} GSP")
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.element.click()
            return 1

        except NoSuchElementException:

            try:
                xpath = f"//a[@class='variable-option pointer']//span[text()='{self.gsp_name}']"
                logger.info(f"Selecting the {self.gsp_name} GSP")
                self.element = self.driver.find_element(By.XPATH, xpath)
                self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.element.click()
            except NoSuchElementException:
                logger.debug("No clickable GSP name is found")
                return None
            else:
                return 1
    
    def check_gsp_title_match(self):
        """Checking if the GSP name and ttile of dashboard matches"""
        try:
            xpath = "//div[contains(@class, 'markdown-html css-fb3dw2')]"
            self.element = self.driver.find_element(By.XPATH, xpath)
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except NoSuchElementException:
            logger.debug("Please check if the page is loaded!")
        else:
            print(self.gsp_name)
            print(self.element.text)            
            if self.gsp_name in self.element.text:
                return 1
            else:
                logger.debug(f"{self.gsp_name} does not match with the dashboard GSP")
                return None

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
            return None

        else:
            # Finding the drop down of GSP names
            xpath = "//span[contains(@aria-label, 'Dashboard template variables')]"
            self.elements = self.driver.find_elements(By.XPATH, xpath)
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

            # Getting each gsp name
            for element in self.elements:
                gsp_names.append(element.text)

        return gsp_names
