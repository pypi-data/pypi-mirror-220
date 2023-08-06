"""
Utility functions for extracting query URLs from a webpage URL.
"""

from time import sleep
from typing import List

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


def _scroll2bottom(driver: webdriver.Chrome) -> None:
    """
    Scroll to the bottom of the page to
    trigger progressive rendering of the content.
    """

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "openAssetPreviewWindow"))
        )
        anchor_elements = driver.find_elements(By.CLASS_NAME, "openAssetPreviewWindow")
    except TimeoutException as e:
        print("Error: Page not loaded after 20 seconds at", driver.current_url)
        raise e

    # Get all image preview link elements.
    previous_links_num = len(anchor_elements)
    # If nothing is rendered, retry triggering the rendering n_repeat times.
    n_repeat = 6
    while n_repeat != 0:
        # Scroll to the bottom.
        driver.execute_script(
            "document.documentElement.scrollTop = document.documentElement.scrollHeight"
        )
        # Wait 6 seconds for the page to render.
        sleep(6)

        current_links_num = len(
            driver.find_elements(By.CLASS_NAME, "openAssetPreviewWindow")
        )

        if previous_links_num < current_links_num:
            previous_links_num = current_links_num
            n_repeat = 6
            continue

        n_repeat -= 1


def _parse_query_url(preview_article_element: WebElement) -> str:
    """Parse a query from an HTML element"""

    anchor_element = preview_article_element.find_element(
        By.CSS_SELECTOR, ".assetWrap .openAssetPreviewWindow"
    )
    return anchor_element.get_attribute("href")


def _extract_queries(driver: webdriver.Chrome, base_url: str) -> List[Query]:
    """Extract queries from a webpage."""

    # Render the webpage and scroll to bottom
    # to trigger the rendering of all the elements.
    driver.get(base_url)
    _scroll2bottom(driver)

    preview_article_elements = driver.find_elements(By.CSS_SELECTOR, "article.asset")
    return [
        {
            "baseUrl": base_url,
            "queryUrl": _parse_query_url(d),
        }
        for d in preview_article_elements
    ]


def fetch_queries(base_urls: List[str], query_path: str) -> None:
    base_fetch_queries(base_urls, query_path, _extract_queries)
