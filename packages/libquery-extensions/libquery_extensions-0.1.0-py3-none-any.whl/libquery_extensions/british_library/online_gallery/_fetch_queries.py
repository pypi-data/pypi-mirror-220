"""
Utility functions for extracting query URLs from a webpage URL.
"""

from time import sleep
from typing import List, Union

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .._utils.fetch_queries import (
    fetch_queries as base_fetch_queries,
    Query,
)
from ._utils import try_switch_to_replay_iframe


def _prefix_href(href: Union[str, None], driver: webdriver.Chrome) -> Union[str, None]:
    """
    If the drive is currently on a webarchive page,
    add webarchive URL to the href.
    """

    if href is None:
        return None

    webarchive_prefix = ""
    if "https://www.webarchive.org.uk/wayback/archive" in driver.current_url:
        webarchive_prefix = driver.current_url.split("http:")[0]
    return f"{webarchive_prefix}{href}"


def _get_next_page_url(driver: webdriver.Chrome) -> Union[str, None]:
    try:
        pagination_element: WebElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "paginationtop"))
        )
    except TimeoutException as e:
        print("Error: Pagination element not found at", driver.current_url)
        raise e

    try:
        # The next page button has inner text "next".
        next_page_button = pagination_element.find_element(
            By.XPATH, "//a[text()='Next']"
        )
    except NoSuchElementException as e:
        # In the UI, the next page button is the last button among the page buttons.
        # The next page button exists for all the pages, except for the final page.
        return None

    # Example href value:
    # http://gallery.bl.uk/viewall/default.aspx?e=Maps%20of%20Asia&n=20&r=10
    return next_page_button.get_attribute("href")


def _parse_query_url(gallery_item_element: WebElement) -> str:
    return (
        gallery_item_element.find_elements(By.CLASS_NAME, "hubitemtext")[0]
        .find_element(By.TAG_NAME, "a")
        .get_attribute("href")
    )


def _extract_queries(driver: webdriver.Chrome, base_url: str) -> List[Query]:
    """
    Get urls of webpages of items from query page at base_url
    Get next query page based on the next button
    """

    driver.get(base_url)
    try_switch_to_replay_iframe(driver)

    try:
        item_list_element: WebElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "itemlist"))
        )
    except TimeoutException as e:
        print("Error: item list not found at", driver.current_url)
        raise e

    gallery_item_elements = item_list_element.find_elements(
        By.CLASS_NAME, "galleryitem"
    )
    queries = [
        {
            "baseUrl": base_url,
            "queryUrl": _prefix_href(_parse_query_url(d), driver),
        }
        for d in gallery_item_elements
    ]

    next_page_url = _prefix_href(_get_next_page_url(driver), driver)
    if next_page_url is not None and next_page_url != "":
        sleep(3)
        queries += _extract_queries(driver, next_page_url)
    return queries


def fetch_queries(base_urls: List[str], query_path: str) -> None:
    base_fetch_queries(base_urls, query_path, _extract_queries)
