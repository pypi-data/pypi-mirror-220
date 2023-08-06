from uuid import uuid5, UUID

from libquery.typing import MetadataEntry


def get_image_uuid(image_url: str, entry: MetadataEntry) -> str:
    """Get the UUID of the image corresponding to a page."""

    source_name = entry["source"]
    return str(uuid5(UUID(int=0), f"{source_name}/{image_url}"))
