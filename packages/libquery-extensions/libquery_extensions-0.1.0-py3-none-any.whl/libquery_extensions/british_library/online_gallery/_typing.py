"""
The type declarations specific to the `Telefact` data source.
"""

from typing import TypedDict

from libquery.typing import MetadataEntry as BaseMetadataEntry
from typing_extensions import NotRequired

SourceData = TypedDict(
    "SourceData",
    {
        "title": str,
        "Medium": str,
        "Date": str,
        "Scale": str,
        "Genre": str,
        "downloadUrl": str,
        "Publisher": NotRequired[str],
        "Width": NotRequired[str],
        "Length": NotRequired[str],
        "Map scale ratio": NotRequired[str],
    },
)


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""

    sourceData: SourceData
