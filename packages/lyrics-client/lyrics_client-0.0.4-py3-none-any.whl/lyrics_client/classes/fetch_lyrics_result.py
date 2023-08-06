from dataclasses import dataclass
from typing import Optional

__all__ = ["FetchLyricsResult"]

@dataclass
class FetchLyricsResult:
    song_title: str
    song_artists: str
    client: str
    lyrics: Optional[str]
    exception: Optional[Exception] = None