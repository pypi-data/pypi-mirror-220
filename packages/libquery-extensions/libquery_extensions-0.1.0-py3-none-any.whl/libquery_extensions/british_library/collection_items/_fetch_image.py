"""
Fetch images from the urls stored in metadata.
"""

from typing import List

from libquery.typing import ImageQuery
from libquery.utils.image import fetch as base_fetch_image
from ._typing import MetadataEntry
from ._utils import get_image_uuid


def _build_image_queries(metadata: List[MetadataEntry]) -> List[ImageQuery]:
    """Build a list of image urls to query."""

    img_queries = []
    for d in metadata:
        source_data = d["sourceData"]
        if "images" not in source_data:
            continue
        img_queries += [
            {
                "url": image_url,
                "uuid": get_image_uuid(image_url, d),
            }
            for image_url in source_data["images"]
        ]
    return img_queries


def fetch_image(metadata_path: str, img_dir: str) -> None:
    return base_fetch_image(metadata_path, img_dir, _build_image_queries)
