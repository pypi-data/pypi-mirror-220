"""
The type declarations specific to the `Alabama Maps` data source.
"""

from typing import TypedDict, Union

from libquery.typing import MetadataEntry as BaseMetadataEntry


class SourceData(TypedDict):
    """The data directly returned from the url."""

    mainAuthor: Union[str, None]
    titleDescription: str
    publicationInfo: str
    date: str
    scale: str
    originalSource: str
    viewUrl: str
    downloadUrl: str


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""

    sourceData: SourceData
