"""
Utility functions for extracting query URLs from a webpage URL.
"""

from time import sleep
from typing import List, Union

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .._utils.fetch_queries import (
    fetch_queries as base_fetch_queries,
    Query,
)


def _get_next_page_url(driver: webdriver.Chrome) -> Union[str, None]:
    """
    The extract the URL of the next page from the next page button.
    Example page: <https://www.bl.uk/collection-items>.
    """

    page_list_element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pageList"))
    )

    # The page buttons.
    page_elements = page_list_element.find_elements(By.TAG_NAME, "a")

    if len(page_elements) == 0:
        return None

    # In the UI, the next page button is the last button among the page buttons.
    # The next page button exists for all the pages, except for the final page.
    last_button = page_elements[-1]
    last_button_content = last_button.find_elements(By.CLASS_NAME, "sr-only")
    has_next_page_button = (
        len(last_button_content) > 0
        and last_button_content[0].get_attribute("innerText") == "Next"
    )
    if has_next_page_button:
        # Example href value:
        # https://www.bl.uk/collection-items?page=2
        next_page_url = last_button.get_attribute("href")
        assert next_page_url.startswith(
            "https://www.bl.uk/collection-items?page="
        ), f"Invalid next page url: {next_page_url}"
        return next_page_url

    return None


def _get_media_card_elements(driver: webdriver.Chrome) -> List[WebElement]:
    try:
        page = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sound-story"))
        )
    except TimeoutException as e:
        print("Error: sound-story not found at", driver.current_url)
        raise e
    return page.find_elements(By.CLASS_NAME, "media-card")


def _parse_query_url(media_card_element: WebElement) -> str:
    """
    Parse a query from an HTML element.

    The href value of the HTML element always follow the pattern:
    fr'https://www.bl.uk/({kebab_case_word}/)?collection-items/{kebab_case_word}'
    where kebab_case_word = '([a-z]+-)*([a-z])*'
    """

    # Example href value:
    # https://www.bl.uk/collection-items/13th-century-english-book-of-hours
    return media_card_element.get_attribute("href")


def _extract_queries(driver: webdriver.Chrome, base_url: str) -> List[Query]:
    """
    Get urls of webpages of items from query page at page_url
    Get next query page based on the next button
    """

    driver.get(base_url)

    media_card_elements = _get_media_card_elements(driver)
    queries = [
        {
            "baseUrl": base_url,
            "queryUrl": _parse_query_url(d),
        }
        for d in media_card_elements
    ]

    next_page_url = _get_next_page_url(driver)
    if next_page_url is not None:
        sleep(3)
        queries += _extract_queries(driver, next_page_url)
    return queries


def fetch_queries(base_urls: List[str], query_path: str) -> None:
    base_fetch_queries(base_urls, query_path, _extract_queries)
