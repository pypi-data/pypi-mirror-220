"""
The type declarations specific to the `Telefact` data source.
"""

from typing import TypedDict

from libquery.typing import MetadataEntry as BaseMetadataEntry
from typing_extensions import NotRequired


SourceData = TypedDict(
    "SourceData",
    {
        "assetName": str,
        "downloadUrl": str,
        "Source": NotRequired[str],
        "Caption": NotRequired[str],
        "Title of Work": NotRequired[str],
        "Shelfmark": NotRequired[str],
        "Place and date of production": NotRequired[str],
        "Credit": NotRequired[str],
        "Artist/creator": NotRequired[str],
        "Author": NotRequired[str],
    },
)


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""

    sourceData: SourceData
