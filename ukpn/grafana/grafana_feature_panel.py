"""Navigate through feature (Voltage, Metered Power Generation etc.) panels of the dashboard """
import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ukpn.grafana.grafana_main_panel import main_panel

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)


class feature_panel(main_panel):
    """Functions to navigate fature panels"""

    def __init__(self) -> None:
        """Functions to configure and select features"""
        super().__init__()

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
            return None
