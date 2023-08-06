"""
Fetch images from the urls stored in metadata.
"""

from typing import List

from libquery.typing import ImageQuery
from libquery.utils.image import fetch as base_fetch_image

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


def fetch_image(metadata_path: str, img_dir: str) -> None:
    return base_fetch_image(metadata_path, img_dir, _build_image_queries)
