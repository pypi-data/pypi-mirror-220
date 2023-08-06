"""
The entrance to querier class.
"""

from typing import List

from libquery.base import BaseQuerier
from libquery.typing import ImageQuery
from libquery.utils.image import fetch as fetch_image

from ._fetch_metadata import fetch_metadata
from ._typing import MetadataEntry


def _build_image_queries(metadata: List[MetadataEntry]) -> List[ImageQuery]:
    """Build a list of image urls to query."""

    return [
        {
            "url": d["sourceData"]["downloadUrl"],
            "uuid": d["uuid"],
        }
        for d in metadata
    ]


class Querier(BaseQuerier):
    def __init__(self, metadata_path: str, img_dir: str):
        self.metadata_path = metadata_path
        self.img_dir = img_dir

    def fetch_metadata(self, queries: List[str]) -> None:
        fetch_metadata(queries, self.metadata_path)

    def fetch_image(self) -> None:
        fetch_image(self.metadata_path, self.img_dir, _build_image_queries)
