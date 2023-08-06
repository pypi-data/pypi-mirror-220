"""
Utility functions for getting metadata from Alabama Maps.
"""

import os
import json
from datetime import datetime, timezone
from typing import List, Union
from urllib import parse
from uuid import uuid5, UUID

import backoff
from libquery.utils.jsonl import load_jl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from ..get_chrome_driver import get_chrome_driver
from ._typing import MetadataEntry, SourceData


def _get_id_in_source(query):
    """
    Split the query part from the url.
    """
    return query.split("/")[-2].split(".")[0]


def _parse_download_url(view_url: str, driver: webdriver.Chrome) -> str:
    """
    Parse image download URL at the current webpage.
    """

    driver.get(view_url)

    try:
        download_url_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//img"))
        )
    except TimeoutException as e:
        print("Error: Fail to find an image in this page.", driver.current_url)
        raise e

    download_url = download_url_element.get_attribute("src")
    parse_result = parse.urlparse(download_url)
    query = parse.parse_qs(parse_result.query)

    # Decides the resolution of the returned image
    query["lev"] = 0
    # Decides the width of the returned image
    query["wid"] = 5000
    # Decides the height of the returned image
    query["hei"] = 4000

    del query["props"]
    del query["bg"]
    del query["cp"]

    parse_result = parse_result._replace(query=parse.urlencode(query, True))
    return parse.urlunparse(parse_result)


def _get_view_url(element: WebElement) -> str:
    try:
        view_url_element = element.find_element(By.TAG_NAME, "a")
    except NoSuchElementException as e:
        print("Error: Failed to find tag <a>.")
        raise e

    return view_url_element.get_attribute("href")


def _get_metadata(element: WebElement) -> List[str]:
    try:
        tr_elements = element.find_elements(By.CSS_SELECTOR, "tr")
    except NoSuchElementException as e:
        print("Error: Failed to find tr elements.")
        raise e

    attrs = []
    for col in tr_elements:
        try:
            td_elements = col.find_elements(By.XPATH, "./td")
        except NoSuchElementException as e:
            print("Error: Failed to find td elements.")
            raise e

        td = td_elements[-1].text.strip()
        attrs.append(td)

    return attrs


def _extract_metadata_entry(
    element: WebElement,
    base_url: str,
    visited_id_in_source: List[str],
) -> Union[MetadataEntry, None]:
    tr_element = element.find_element(By.XPATH, "./tbody/tr")
    td_elements = tr_element.find_elements(By.XPATH, "./td")
    view_url = _get_view_url(td_elements[0])
    attrs = _get_metadata(td_elements[-1])

    id_in_source = _get_id_in_source(view_url)
    if id_in_source in visited_id_in_source:
        return None

    if view_url.split(".")[-1] == "htm":
        return None

    main_author = attrs[0].strip(" (info)")
    if main_author == "\u00A0":
        main_author = None
    title_description = None if attrs[1] in {"", "\u00A0"} else attrs[1]

    source_data: SourceData = {
        "mainAuthor": main_author,
        "titleDescription": title_description,
        "publicationInfo": attrs[2],
        "date": attrs[3],
        "scale": attrs[4],
        "originalSource": attrs[5],
        "viewUrl": view_url,
        "downloadUrl": "",
    }
    source = "Alabama Maps"
    return {
        "uuid": str(uuid5(UUID(int=0), f"{source}/{id_in_source}")),
        "url": base_url,
        "source": source,
        "idInSource": id_in_source,
        "accessDate": datetime.now(timezone.utc).isoformat(),
        "sourceData": source_data,
    }


def _get_table_elements(driver: webdriver.Chrome) -> List[WebElement]:
    try:
        elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/table"))
        )
    except TimeoutException as e:
        print("Error: Fail to find tables in this page.", driver.current_url)
        raise e

    return elements[2:-1]


def _parse_store_entries(
    driver: webdriver.Chrome,
    base_url: str,
    metadata_path: str,
    visited_id_in_source: List[str],
) -> None:
    driver.get(base_url)
    elements = _get_table_elements(driver)
    for element in elements:
        item = _extract_metadata_entry(element, base_url, visited_id_in_source)
        if item is None:
            continue
        item["sourceData"]["downloadUrl"] = _parse_download_url(
            item["sourceData"]["viewUrl"], driver
        )
        with open(metadata_path, "a") as f:
            f.write(f"{json.dumps(item)}\n")


@backoff.on_exception(
    backoff.constant, (NoSuchElementException, TimeoutException, WebDriverException)
)
def fetch_metadata(base_urls: List[str], metadata_path: str) -> None:
    """
    Given base urls, generate metadata queries, and store the query results.

    Args
    ----
    base_urls : List[str]
        The base urls for generating queries.
        Each base url corresponds to a search keyword.
    metadata_path : str
        The path to the metadata file.
    """

    # The directory containing the metadata file.
    directory = os.path.dirname(metadata_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    visited_id_in_source = (
        []
        if not os.path.exists(metadata_path)
        else [d["idInSource"] for d in load_jl(metadata_path)]
    )
    driver = get_chrome_driver()
    for base_url in tqdm(base_urls, desc="Fetch Metadata Progress"):
        _parse_store_entries(
            driver,
            base_url,
            metadata_path,
            visited_id_in_source,
        )
