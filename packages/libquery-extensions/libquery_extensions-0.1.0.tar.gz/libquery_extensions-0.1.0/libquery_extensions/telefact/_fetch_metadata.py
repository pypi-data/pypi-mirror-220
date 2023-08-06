"""
Utility functions for getting metadata from Telefact.
"""

import os
import json
import re
from calendar import month_abbr
from datetime import datetime, timezone
from typing import List
from uuid import uuid5, UUID

import backoff
import requests
from libquery.utils.jsonl import load_jl
from requests import Response
from requests.exceptions import ProxyError
from tqdm import tqdm

from ._typing import MetadataEntry, TimePoint


month_str_to_num = {month: index for index, month in enumerate(month_abbr) if month}


def _build_queries(base_urls: List[str], save_path: str) -> List[str]:
    """
    Build a list of urls to query.
    The urls already queried according to
    the stored metadata will be excluded.
    """

    # Load progress.
    entries = [] if not os.path.exists(save_path) else load_jl(save_path)
    queried_urls = {d["url"] for d in entries}
    return [d for d in base_urls if d not in queried_urls]


def _get_image_url(html_text: str) -> str:
    """Extract image url from the html."""

    image_url_pattern = re.compile(r'<img class="img" src="(.*?)"')
    matches = image_url_pattern.findall(html_text)
    assert len(matches) == 1, f"length = {len(matches)}"
    return matches[0]


def _get_publish_date(html_text: str) -> TimePoint:
    """
    Return the publish date (year, month, day).

    Notes
    -----
    The element is the only <p> in the webpage.
    pattern examples:
    <p>Rudolf modley-pictograph corporation-telefact-Mon__Feb_10__1941_</p>
    <p>Rudolf modley -pictograph corporation-telefact-Sat__Dec_13__1941</p>
    <p>Rudolf modley-pictograph corporation-telefact-Apr_11__1941_</p>
    <p>Rudolf modley-pictograph corporation-telefact_Sat__Oct_18__1941_</p>
    <p>Rudolf modley-pictograph corporation-telefact-Tue__Nov_26__1940_.png</p>
    <p>Rudolf modley-pictograph corporation-Wed__May_31__1939_</p>
    <p>Rudolf modley-pictograph corporation_Wed__Feb_15__1939_ (1)</p>
    <p>Rudolf modley-pictograph corporation -Wed__May_31__1939_</p>
    <p>Wed__Oct_19__1938</p>
    """

    publish_date_pattern = re.compile(r"<p>(.*?)</p>")
    matches = publish_date_pattern.findall(html_text)
    assert len(matches) == 1, f"length = {len(matches)}"
    publish_date_str = matches[0]

    # clean the string
    publish_date_str = (
        publish_date_str.replace("Rudolf modley", "")
        .replace("-pictograph corporation", "")
        .replace("-telefact", "")
        .replace("-", "")
        .replace(".png", "")
        .replace("__", "_")
        .lstrip()
        .split(" ")[0]
    )
    segments = publish_date_str.split("_")
    segments = [d for d in segments if d != ""]

    if len(segments) == 4:
        month = month_str_to_num[segments[1]]
        day = int(segments[2])
        year = int(segments[3])
    elif len(segments) == 3:
        month = month_str_to_num[segments[0]]
        day = int(segments[1])
        year = int(segments[2])
    else:
        raise ValueError(f"Cannot parse date {publish_date_str}")

    return {
        "year": year,
        "month": month,
        "day": day,
    }


def __get_id_in_source(query: str) -> str:
    """Extract idInSource from the query."""
    return query.split("/")[-2]


def _parse(response: Response) -> MetadataEntry:
    """
    Parse metadata of entries in Telefact.
    """

    html_text = response.text

    # Try parsing the html text.
    try:
        image_url = _get_image_url(html_text)
        publish_date = _get_publish_date(html_text)
    except Exception as e:
        raise ValueError(f"Fail to parse url: {response.url}") from e

    source = "Telefact"
    id_in_source = __get_id_in_source(response.url)

    return {
        "uuid": str(uuid5(UUID(int=0), f"{source}/{id_in_source}")),
        "url": response.url,
        "source": source,
        "idInSource": id_in_source,
        "accessDate": datetime.now(timezone.utc).isoformat(),
        "sourceData": {
            "authors": ["Modley, Rudolf"],
            "publishDate": publish_date,
            "viewUrl": response.url,
            "downloadUrl": image_url,
            "languages": ["eng"],
        },
    }


@backoff.on_exception(backoff.constant, ProxyError)
def fetch_metadata(
    base_urls: List[str], metadata_path: str, html_dir: str = None
) -> None:
    """
    Given base urls, generate metadata queries, and store the query results.

    Args
    ----
    base_urls : List[str]
        The base urls for generating queries.
        Each base url corresponds to a search keyword.
    metadata_path : str
        The path to the metadata file.
    html_dir : str or None
        The directory to store the HTML files returned for each query.
        The HTML files serve the debugging purpose.
        If None, do not store the HTML files.
    """

    s = requests.Session()

    # The directory containing the metadata file.
    output_dir = os.path.dirname(metadata_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    queries = _build_queries(base_urls, metadata_path)

    if html_dir is not None and not os.path.exists(html_dir):
        os.makedirs(html_dir)

    for query in tqdm(queries, desc="Fetch Metadata Progress"):
        response = s.get(query)
        metadata_entry = _parse(response)

        if html_dir is not None:
            uuid = metadata_entry["uuid"]
            with open(f"{html_dir}/{uuid}.html", "w", encoding="utf-8") as f:
                f.write(response.text)

        with open(metadata_path, "a", encoding="utf-8") as f:
            f.write(f"{json.dumps(metadata_entry)}\n")
