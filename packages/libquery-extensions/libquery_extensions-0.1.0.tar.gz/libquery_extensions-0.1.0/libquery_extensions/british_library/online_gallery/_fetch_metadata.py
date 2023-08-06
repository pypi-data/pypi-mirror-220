"""
Utility functions for getting metadata from British Library
"""

from typing import Dict, Union

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .._utils.fetch_metadata import fetch_metadata as base_fetch_metadata
from ._utils import try_switch_to_replay_iframe


def _get_image_url(driver: webdriver.Chrome) -> str:
    try:
        image_link_wrapper: WebElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "imagelinkwrapper"))
        )
    except TimeoutException as e:
        print("Error: image link not found at", driver.current_url)
        raise e

    try:
        full_size_button = image_link_wrapper.find_element(
            By.XPATH, "//a[text()='Full size printable image']"
        )
    except NoSuchElementException as e:
        print("Error: full size button not found at", driver.current_url)
        raise e

    full_image_url = full_size_button.get_attribute("href")

    driver.get(full_image_url)
    try_switch_to_replay_iframe(driver)

    try:
        image_element: WebElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#largeimage img"))
        )
    except TimeoutException as e:
        print("Error: large image not found at", driver.current_url)
        raise e

    # Replace HTTP protocol with HTTPS
    src = image_element.get_attribute("src")
    src = "https://" + src.lstrip("http://")
    return src


def _get_attributes_from_table(driver: webdriver.Chrome) -> Dict[str, str]:
    """Parse attributes from the description table."""

    try:
        item_text_wrapper: WebElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "itemtextwrapper"))
        )
    except TimeoutException as e:
        print("Error: item text not found at", driver.current_url)
        raise e

    attributes = {}
    item_metadata_elements = item_text_wrapper.find_elements(
        By.CSS_SELECTOR, "[id='itemmetadata'] p"
    )
    for element in item_metadata_elements:
        item_text = element.get_attribute("innerText")
        item_key = item_text.split(":")[0]
        item_value = ":".join(item_text.split(":")[1:]).lstrip(" ")
        attributes[item_key] = item_value
    return attributes


def _get_title(driver: webdriver.Chrome) -> Union[str, None]:
    """
    Note that not all the image collection items have short description.
    Example: <https://www.bl.uk/collection-items/american-revolution-boston-massacre>
    """

    try:
        title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#contenttop h1"))
        )
    except TimeoutException:
        return None
    return title_element.get_attribute("innerText")


def _extract_source_data(driver: webdriver.Chrome):
    try_switch_to_replay_iframe(driver)
    return {
        "title": _get_title(driver),
        **_get_attributes_from_table(driver),
        "downloadUrl": _get_image_url(driver),
    }


def fetch_metadata(query_path: str, metadata_path: str, html_dir: str = None) -> None:
    return base_fetch_metadata(
        query_path, metadata_path, _extract_source_data, html_dir
    )
