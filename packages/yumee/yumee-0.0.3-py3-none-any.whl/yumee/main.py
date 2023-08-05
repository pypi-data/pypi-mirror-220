from pathlib import Path
from taipan_di import ServiceCollection

from yumee.di import add_yumee
from yumee.errors import SongMetadataFileError
from yumee.interfaces import BaseSongFile, BaseSongFileProvider

__all__ = ["SongMetadataEmbedder"]


class SongMetadataEmbedder:
    def __init__(self) -> None:
        services = ServiceCollection()
        add_yumee(services)
        provider = services.build()

        self._provider = provider.resolve(BaseSongFileProvider)

    def open_file(self, path: Path) -> BaseSongFile:
        song_file = self._provider.exec(path)

        if song_file is None:
            raise SongMetadataFileError(
                f"Couldn't open file at path {path}. The extension might not be supported."
            )

        return song_file
