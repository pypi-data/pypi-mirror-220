"""
Utility functions for getting metadata from British Library
"""

import json
import os
from datetime import datetime, timezone
from time import sleep
from typing import Any, Callable, List
from uuid import uuid5, UUID

import backoff
from libquery.typing import MetadataEntry
from libquery.utils.jsonl import load_jl
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from tqdm import tqdm

from ...get_chrome_driver import get_chrome_driver
from .fetch_queries import Query


def build_queries(query_path: str, metadata_path: str) -> List[Query]:
    """
    Build a list of urls to query.
    The urls have not been queried before
    according to the stored metadata.
    """

    # Load all the page queries.
    queries = load_jl(query_path)

    # Load page urls already visited.
    entries = [] if not os.path.exists(metadata_path) else load_jl(metadata_path)
    queried_urls = {d["url"] for d in entries}

    # Discard the page queries with urls already visited.
    queries = [d for d in queries if d["queryUrl"] not in queried_urls]

    # Deduplicate page queries with the same urls.
    return {d["queryUrl"]: d for d in queries}.values()


def parse(
    query: str,
    driver: webdriver.Chrome,
    extract_source_data: Callable[[webdriver.Chrome], Any],
) -> MetadataEntry:
    """
    Parse metadata of entries.
    """

    source_name = "British Library"
    # Use the query url as idInSource.
    id_in_source = query

    return {
        "uuid": str(uuid5(UUID(int=0), f"{source_name}/{id_in_source}")),
        "url": query,
        "source": source_name,
        "idInSource": id_in_source,
        "accessDate": datetime.now(timezone.utc).isoformat(),
        "sourceData": extract_source_data(driver),
    }


@backoff.on_exception(backoff.constant, (TimeoutException, WebDriverException))
def fetch_metadata(
    query_path: str,
    metadata_path: str,
    extract_source_data: Callable[[webdriver.Chrome], Any],
    html_dir: str = None,
) -> None:
    """
    Read base urls from stored files, generate metadata queries,
    and store the query results.

    Args
    ----
    query_path : str
        The path to the file storing URLs.
    metadata_path : str
        The path to the metadata file.
    html_dir : str or None
        The directory to store the HTML files returned for each query.
        The HTML files serve the debugging purpose.
        If None, do not store the HTML files.
    """

    driver = get_chrome_driver()

    # The directory containing the metadata file.
    output_dir = os.path.dirname(metadata_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create empty metadata file.
    open(metadata_path, "a").close()

    queries = build_queries(query_path, metadata_path)
    queries = [d["queryUrl"] for d in queries]

    if html_dir is not None and not os.path.exists(html_dir):
        os.makedirs(html_dir)

    for query in tqdm(queries, desc="Fetch Metadata Progress"):
        driver.get(query)
        metadata_entry = parse(query, driver, extract_source_data)

        if html_dir is not None:
            uuid = metadata_entry["uuid"]
            with open(f"{html_dir}/{uuid}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

        with open(metadata_path, "a", encoding="utf-8") as f:
            f.write(f"{json.dumps(metadata_entry)}\n")

        sleep(3)

    driver.close()
