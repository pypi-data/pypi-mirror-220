"""
Utility functions for extracting query URLs from a webpage URL.
"""

import json
import os
from typing import Any, Callable, List, TypedDict, Set

import backoff
from libquery.utils.jsonl import load_jl
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm

from ...get_chrome_driver import get_chrome_driver


class Query(TypedDict):
    # The url from which the query url is extracted.
    baseUrl: str
    # The extracted query url.
    queryUrl: str


def _append_jl(data: List[Any], path: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        for d in data:
            f.write(f"{json.dumps(d, ensure_ascii=False)}\n")


def _get_visited_base_urls(query_path: str) -> Set[str]:
    if not os.path.exists(query_path):
        return set()
    queries: Query = load_jl(query_path)
    return {d["baseUrl"] for d in queries}


@backoff.on_exception(backoff.constant, WebDriverException)
def fetch_queries(
    base_urls: List[str],
    query_path: str,
    _extract_queries: Callable[[webdriver.Chrome, str], Query],
) -> None:
    """
    Fetch and save queries to be accomplished.

    When the network is disconnected, which causes WebDriverException,
    the fetch operation will be retried.
    """

    path_dir = os.path.dirname(query_path)
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    # Create empty query file.
    open(query_path, "a").close()

    driver = get_chrome_driver()
    visited_base_urls = _get_visited_base_urls(query_path)
    for base_url in tqdm(base_urls, desc="Fetch Queries Progress"):
        if base_url in visited_base_urls:
            continue
        queries = _extract_queries(driver, base_url)
        _append_jl(queries, query_path)
    driver.close()
