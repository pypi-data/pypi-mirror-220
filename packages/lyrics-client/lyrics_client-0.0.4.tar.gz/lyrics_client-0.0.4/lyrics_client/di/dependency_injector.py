from taipan_di import ServiceCollection

from lyrics_client.interfaces import BaseLyricsClient
from lyrics_client.classes.clients import GeniusLyricsClient, AZLyricsLyricsClient, MusixmatchLyricsClient

__all__ = ["add_lyrics_client"]

def add_lyrics_client(services: ServiceCollection) -> ServiceCollection:
    services.register_pipeline(BaseLyricsClient)\
        .add(GeniusLyricsClient)\
        .add(AZLyricsLyricsClient)\
        .add(MusixmatchLyricsClient)\
        .as_factory()
    
    return services