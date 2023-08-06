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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .._utils.fetch_metadata import fetch_metadata as base_fetch_metadata


def _get_image_url(driver: webdriver.Chrome) -> str:
    """
    Extract image download URL from the webpage.
    The webpage is expected to have one image.
    """

    try:
        # Wait for the image element to render.
        # Note: there can be one or multiple image elements.
        img_element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".imageHugger img"))
        )
    except NoSuchElementException as e:
        print("Error: no image detected at", driver.current_url)
        raise e

    image_url = img_element.get_attribute("src")

    if isinstance(image_url, list):
        raise ValueError(
            "Error: Multiple images detected on the webpage:", driver.current_url
        )

    return image_url


def _get_asset_name(driver: webdriver.Chrome) -> Union[str, None]:
    return driver.find_element(By.CLASS_NAME, "assetName").get_attribute("innerText")


def _get_additional_attributes(driver: webdriver.Chrome) -> Dict[str, str]:
    """Extract additional attributes from the webpage."""

    try:
        asset_detail_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".previewAssetDetailsItem")
            )
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".detail"))
        )
        asset_detail_spans = asset_detail_div.find_elements(By.CSS_SELECTOR, ".detail")
    except TimeoutException as e:
        print("Error: Item details not found at", driver.current_url)
        raise e

    additional_attributes = {}
    for span in asset_detail_spans:
        try:
            label = (
                span.find_element(By.CSS_SELECTOR, ".label")
                .get_attribute("innerText")
                .split(":")[0]
            )
            value = span.find_element(By.CSS_SELECTOR, ".desc").get_attribute(
                "innerText"
            )
            additional_attributes[label] = value
        except NoSuchElementException as e:
            print("Error: label and value not matching at", driver.current_url)
            raise e

    return additional_attributes


def _extract_source_data(driver: webdriver.Chrome):
    return {
        "assetName": _get_asset_name(driver),
        **_get_additional_attributes(driver),
        "downloadUrl": _get_image_url(driver),
    }


def fetch_metadata(query_path: str, metadata_path: str, html_dir: str = None) -> None:
    return base_fetch_metadata(
        query_path, metadata_path, _extract_source_data, html_dir
    )
