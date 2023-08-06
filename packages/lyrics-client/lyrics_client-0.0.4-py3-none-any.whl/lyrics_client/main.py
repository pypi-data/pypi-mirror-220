from typing import List
from taipan_di import ServiceCollection

from lyrics_client.classes import FetchLyricsCommand, FetchLyricsResult
from lyrics_client.di import add_lyrics_client
from lyrics_client.interfaces import BaseLyricsClient
from lyrics_client.errors import NoResultError

__all__ = ["LyricsClient"]


class LyricsClient:
    def __init__(self):
        services = ServiceCollection()
        add_lyrics_client(services)

        self._clients = services.build().resolve(BaseLyricsClient)

    def get_lyrics(self, request: FetchLyricsCommand) -> List[FetchLyricsResult]:
        result = self._clients.exec(request)

        if result is None:
            raise NoResultError("No result")

        return result

    def get_from_song(
        self, song_title: str, song_artists: str, clients: List[str] = ["genius"]
    ) -> List[FetchLyricsResult]:
        command = FetchLyricsCommand(song_title, song_artists, clients)
        return self.get_lyrics(command)
