"""
The entrance to querier class.
"""

from typing import List

from libquery.base import BaseQuerier

from ._fetch_image import fetch_image
from ._fetch_metadata import fetch_metadata
from ._fetch_queries import fetch_queries


class Querier(BaseQuerier):
    """
    The querier for the `British Library Online Gallery` data source.
    """

    def __init__(self, query_path: str, metadata_path: str, img_dir: str):
        self.query_path = query_path
        self.metadata_path = metadata_path
        self.img_dir = img_dir

    def fetch_metadata(self, base_urls: List[str], html_dir: str = None) -> None:
        fetch_queries(base_urls, self.query_path)
        fetch_metadata(self.query_path, self.metadata_path, html_dir=html_dir)

    def fetch_image(self) -> None:
        fetch_image(self.metadata_path, self.img_dir)
