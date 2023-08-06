"""
The type declarations specific to the `Telefact` data source.
"""

from typing import List, Literal, TypedDict

from typing_extensions import NotRequired
from libquery.typing import MetadataEntry as BaseMetadataEntry


class TimePoint(TypedDict):
    """The time point data structure."""

    year: int
    month: NotRequired[int]
    day: NotRequired[int]


class SourceData(TypedDict):
    """The data directly returned from the url."""

    authors: List[Literal["Modley, Rudolf"]]
    publishDate: TimePoint
    downloadUrl: str
    languages: List[Literal["eng"]]


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""

    sourceData: SourceData
