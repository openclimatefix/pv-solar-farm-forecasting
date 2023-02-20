"""Initiating Chrome webdriver using Selenium Python"""
import logging
import os
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger_webdriver = logging.getLogger("selenium.webdriver.remote.remote_connection")
logger_webdriver.setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)


def get_chrome():
    """Search for the Chrome driver folder'"""
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


class open_webpage:
    """Setting up the Chrome options"""

    def __init__(
        self,
        download_directory: str = None,
        url_link: str = "https://dsodashboard.ukpowernetworks.co.uk",
    ) -> None:
        """Function to set the desired chrome options"""
        self.download_directory = download_directory
        self.url_link = url_link
        self.prefs = {
            "download.default_directory": f"{self.download_directory}",
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

    def Initialise_chrome(self) -> None:
        """Initalise the chrome browser"""
        try:
            logger.info("Driver is getting downloaded")
            # Download the browser
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=self.opts
            )

            # Setting up a wait period of 30 seconds for browser operations
            self.wait = WebDriverWait(self.driver, 30)

            # Open the link in a tab
            self.driver.get(self.url_link)
            self.driver.implicitly_wait(15)
            self.driver.maximize_window()

            # Wait until the page is loaded
            try:
                xpath = "//div[@class='navbar-page-btn']"
                self.element = self.driver.find_element(By.XPATH, xpath)
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            except NoSuchElementException:
                logger.debug("Webpage load unsucessfull!")
                logger.debug("Increase loading and waiting time!")
            else:
                # Checking the website load status
                title = self.driver.title
                if title is None:
                    logger.debug("Webpage loading unsuccessful!")
                    logger.debug(f"Check URL - {self.url_link}")
                    return None

        except TimeoutException:
            logger.debug("Page load timeout occured!")
            logger.debug("Check the url link!")
            self.driver.refresh()
            return None
        else:
            return 1

    def close_or_refresh(
        self, refresh_window: Optional[bool] = False, close_browser: Optional[bool] = False
    ):
        """Function to refresh or close the browser"""
        # Option to refresh the browser
        try:
            if refresh_window:
                self.driver.refresh()
                logger.info("Browser window refreshed!")
            if close_browser:
                self.driver.close()
                logger.info("Browser closed!")
        except InvalidSessionIdException:
            logger.debug("There is no browser to be closed!")
            return None
        else:
            return 1
