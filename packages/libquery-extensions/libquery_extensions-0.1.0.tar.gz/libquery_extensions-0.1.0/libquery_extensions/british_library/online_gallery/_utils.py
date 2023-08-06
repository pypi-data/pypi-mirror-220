from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def try_switch_to_replay_iframe(driver: webdriver.Chrome) -> None:
    """
    Get into the replay iframe that present when the webpage is
    archived by webarchive.org.uk.

    Example:
    https://www.webarchive.org.uk/wayback/archive/20160109092723/http://www.bl.uk/onlinegallery/onlineex/maps/asia/5000647.html
    """

    try:
        # If replay iframe exists, switch to the iframe to extract data.
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "replay_iframe"))
        )
        driver.switch_to.frame("replay_iframe")
    except TimeoutException:
        # If the iframe does not exist, use to whole page to extract data.
        pass
