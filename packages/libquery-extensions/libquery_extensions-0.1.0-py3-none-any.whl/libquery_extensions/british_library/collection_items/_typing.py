"""
The type declarations specific to the `British Library Collection Items` data source.
"""

from typing import List, TypedDict

from libquery.typing import MetadataEntry as BaseMetadataEntry
from typing_extensions import NotRequired


Item = TypedDict(
    "Item",
    {
        "Full title": NotRequired[str],
        "Published": NotRequired[str],
        "Locations": NotRequired[str],
        "Created": NotRequired[str],
        "Format": NotRequired[str],
        "Language": NotRequired[str],
        "Creator": NotRequired[str],
        "Usage terms": NotRequired[str],
        "Held by": NotRequired[str],
        "Shelfmark": NotRequired[str],
        "shortDescription": NotRequired[str],
        "Copyright": NotRequired[str],
        "Title": NotRequired[str],
        "Date": NotRequired[str],
        "Duration": NotRequired[str],
        "Publisher": NotRequired[str],
        "Publishers": NotRequired[str],
        "Track/Part": NotRequired[str],
    },
)


class SourceData(TypedDict):
    """The data directly returned from the url."""

    item: Item
    images: NotRequired[List[str]]


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""

    sourceData: SourceData
