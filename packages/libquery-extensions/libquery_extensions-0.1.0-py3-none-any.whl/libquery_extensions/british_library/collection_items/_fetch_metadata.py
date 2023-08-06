"""
Utility functions for getting metadata from British Library
"""

import codecs
import re
from typing import List, Union, Dict

import cssutils
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .._utils.fetch_metadata import fetch_metadata as base_fetch_metadata
from ._typing import SourceData


def _cleansing_text(text: str) -> str:
    text = codecs.getdecoder("unicode_escape")(text)[0]
    text = re.sub(
        r"[\xc2-\xf4][\x80-\xbf]+",
        lambda m: m.group(0).encode("latin1").decode("utf8"),
        text,
    )
    text = text.replace("\xa0", " ")
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = text.strip()
    text = re.sub(" +", " ", text)
    return text


def _parse_url_from_background(background: str) -> str:
    """Parse URL from css background."""

    return background.rstrip("'\");").lstrip("url('\"")


def _get_image_urls_from_thumbnails(driver: webdriver.Chrome) -> List[str]:
    """
    Get image urls from image thumbnails.

    An example is five image thumbnails in
    <https://www.bl.uk/collection-items/1066-and-all-that>.

    Note that even when the image thumbnails are not visible,
    they will still exist in the DOM, as in
    <https://www.bl.uk/collection-items/tarjumah-kimiya-e-saadat>.

    Only pages of collections with multiple images have image thumbnails.
    A counter example with no image thumbnails is
    <https://www.bl.uk/collection-items/octopium-landlordicuss>.
    """

    try:
        indicators_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "indicators"))
        )
    except TimeoutException:
        return []

    image_elements = indicators_element.find_elements(By.CSS_SELECTOR, ".image")
    image_urls = []
    for element in image_elements:
        image_style = element.get_attribute("style")
        background = cssutils.parseStyle(image_style)["background"]
        image_urls.append(_parse_url_from_background(background))
    return image_urls


def _get_image_url_from_container(driver: webdriver.Chrome) -> Union[str, None]:
    try:
        image_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".image-container img"))
        )
    except TimeoutException as e:
        # Note that image collection may have 0 images, as is the case in the following example.
        # <https://www.bl.uk/speaking-out/collection-items/not-cleared-spo62-aneurin-bevan-1959-election-speech>.
        return None

    return image_div.get_attribute("src")


def _get_image_urls(driver: webdriver.Chrome) -> List[str]:
    try:
        image_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "imageBadge"))
        )
        image_button.click()
    except TimeoutException as e:
        print("Error: Fail to click image viewing button at", driver.current_url)
        raise e

    image_urls = _get_image_urls_from_thumbnails(driver)
    if len(image_urls) != 0:
        return image_urls
    image_url = _get_image_url_from_container(driver)
    return [image_url] if image_url is not None else []


def _get_attributes_from_table(driver: webdriver.Chrome) -> Union[Dict[str, str], None]:
    """Parse attributes from the description table."""

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".author-summary tr"))
        )
    except TimeoutException:
        # Note that the entry may not have table cells, as is the case in the following example.
        # <https://www.bl.uk/collection-items/test>
        return None

    tr_elements = driver.find_elements(By.CSS_SELECTOR, ".author-summary tr")
    attributes = {}
    for d in tr_elements:
        td_element = d.find_elements(By.TAG_NAME, "td")
        if len(td_element) != 2:
            continue
        key = td_element[0].get_attribute("innerText").rstrip(": ")
        attributes[key] = td_element[1].get_attribute("innerText")
    return attributes


def _get_short_description(driver: webdriver.Chrome) -> Union[str, None]:
    """
    Note that not all the image collection items have short description.
    Example: <https://www.bl.uk/collection-items/american-revolution-boston-massacre>
    """

    try:
        short_description_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "short-description"))
        )
    except TimeoutException:
        return None
    return _cleansing_text(short_description_element.get_attribute("innerText"))


def _check_is_image(driver: webdriver.Chrome) -> bool:
    """
    Check if the current collection item is a collection of image(s).

    The collection items that are not images
    will not have the 'View images from this item' button, see example
    <https://www.bl.uk/collection-items/1954-film-version-of-animal-farm-by-halas-and-batchelor>.
    """

    try:
        # Image collection should have a 'View images from this item' button.
        image_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "imageBadge"))
        )
        button_text: str = image_button.get_attribute("innerText")
        assert button_text.startswith(
            "View images from this item"
        ), "Invalid button text"
        return True
    except TimeoutException:
        return False


def _extract_source_data(driver: webdriver.Chrome) -> SourceData:
    """
    TODO: Currently, the metadata in the "Full catalogue details" page are not captured.
    For example, for <https://www.bl.uk/collection-items/octopium-landlordicuss>,
    the data in <https://explore.bl.uk/primo_library/libweb/action/dlDisplay.do?vid=BLVU1&afterPDS=true&institution=BL&docId=BLL01015819903>
    are not captured.
    """

    attributes = _get_attributes_from_table(driver)
    source_data = {"item": {}} if attributes is None else {"item": {**attributes}}

    is_image = _check_is_image(driver)
    if not is_image:
        return source_data

    short_description = _get_short_description(driver)
    if short_description is not None:
        source_data["item"]["shortDescription"] = short_description
    source_data["images"] = _get_image_urls(driver)
    return source_data


def fetch_metadata(query_path: str, metadata_path: str, html_dir: str = None) -> None:
    return base_fetch_metadata(
        query_path, metadata_path, _extract_source_data, html_dir
    )
