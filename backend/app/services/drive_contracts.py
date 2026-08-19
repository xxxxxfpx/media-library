"""Provider-neutral contracts for turning a source URL into a playable file."""

from dataclasses import dataclass
from typing import Literal, Protocol


SaveMode = Literal["offline", "upload"]


@dataclass
class SavedFile:
    provider: str
    file_id: str
    url: str
    mode: SaveMode
    name: str | None = None
    size: int | None = None


class UrlSaver(Protocol):
    async def save_url(self, url: str, mode: SaveMode, parent_id: str = "", name: str | None = None) -> SavedFile:
        """Persist a source URL to a provider and return its playable URL."""
