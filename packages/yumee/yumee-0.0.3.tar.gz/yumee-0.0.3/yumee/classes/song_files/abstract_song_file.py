__all__ = ["AbstractSongFile"]

import abc
import logging
from pathlib import Path
from typing import Generic, List, Optional, Tuple, TypeVar

from mutagen._file import FileType

from yumee.data import TagPreset, SongMetadata
from yumee.errors import SongMetadataFileError


T = TypeVar("T", bound=FileType)


class AbstractSongFile(Generic[T], metaclass=abc.ABCMeta):
    def __init__(self, path: Path) -> None:
        self._path = str(path.resolve())
        self._extension = path.suffix
        self._logger: logging.Logger = logging.getLogger("yumee")

        try:
            self._audio_file: T = self._load()
        except Exception as ex:
            raise SongMetadataFileError(ex) from ex
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.save()

    @abc.abstractmethod
    def _load(self) -> T:
        ...

    @property
    @abc.abstractmethod
    def tag_preset(self) -> TagPreset:
        ...

    def save(self) -> None:
        self._audio_file.save()
        self._logger.debug("File at path %s saved !", self._path)
        
    def embed(self, metadata: SongMetadata) -> None:
        if metadata.album_artist:
            self.album_artist = [metadata.album_artist]
        elif metadata.artist:
            self.album_artist = [metadata.artist]

        if metadata.album_name:
            self.album_name = [metadata.album_name]
        if metadata.artists:
            self.artists = metadata.artists
        if metadata.comments:
            self.comments = metadata.comments
        if metadata.copyright_text:
            self.copyright_text = [metadata.copyright_text]
        if metadata.cover_url:
            self.cover_url = metadata.cover_url
        if metadata.date:
            self.date = [metadata.date]
        if metadata.disc_number:
            self.disc_number = (
                metadata.disc_number,
                metadata.disc_count if metadata.disc_count else metadata.disc_number,
            )
        if metadata.explicit:
            self.explicit = metadata.explicit
        if metadata.genres:
            self.genres = metadata.genres
        if metadata.lyrics:
            self.lyrics = [metadata.lyrics]
        if metadata.origin_website:
            self.origin_website = [metadata.origin_website]
        if metadata.publisher:
            self.publisher = [metadata.publisher]
        if metadata.title:
            self.title = [metadata.title]
        if metadata.track_number:
            self.track_number = (
                metadata.track_number,
                metadata.track_count if metadata.track_count else metadata.track_number,
            )
        if metadata.year:
            self.year = metadata.year
            
        self.save()
            
    def extract(self) -> SongMetadata:
        metadata = SongMetadata(
            title=self.title[0] if self.title else None,
            artist=self.artists[0] if self.artists else None,
            artists=self.artists,
            album_name=self.album_name[0] if self.album_name else None,
            album_artist=self.album_artist[0] if self.album_artist else None,
            track_number=self.track_number[0] if self.track_number else None,
            track_count=self.track_number[1] if self.track_number else None,
            disc_number=self.disc_number[0] if self.disc_number else None,
            disc_count=self.disc_number[1] if self.disc_number else None,
            genres=self.genres,
            date=self.date[0] if self.date else None,
            year=self.year,
            explicit=self.explicit,
            cover_url=self.cover_url,
            lyrics=self.lyrics[0] if self.lyrics else None,
            comments=self.comments,
            origin_website=self.origin_website[0] if self.origin_website else None,
            publisher=self.publisher[0] if self.publisher else None,
            copyright_text=self.copyright_text[0] if self.copyright_text else None
        )
        
        return metadata

    # Artists

    @property
    def artists(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.artist)

    @artists.setter
    def artists(self, new_artists: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.artist] = new_artists

    # Album artists

    @property
    def album_artist(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.albumartist)

    @album_artist.setter
    def album_artist(self, new_album_artist: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.albumartist] = new_album_artist

    # Title

    @property
    def title(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.title)

    @title.setter
    def title(self, new_title: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.title] = new_title

    # Date

    @property
    def date(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.date)

    @date.setter
    def date(self, new_date: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.date] = new_date

    # Encoded By / Publisher

    @property
    def publisher(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.encodedby)

    @publisher.setter
    def publisher(self, new_publisher: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.encodedby] = new_publisher

    # Album Name

    @property
    def album_name(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.album)

    @album_name.setter
    def album_name(self, new_album_name: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.album] = new_album_name

    # Genres

    @property
    def genres(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.genre)

    @genres.setter
    def genres(self, new_genres: Optional[List[str]]) -> None:
        if new_genres is None:
            self._audio_file[self.tag_preset.genre] = None
        else:
            self._audio_file[self.tag_preset.genre] = [genre.title() for genre in new_genres]

    # Copyright Text

    @property
    def copyright_text(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.copyright)

    @copyright_text.setter
    def copyright_text(self, new_copyright_text: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.copyright] = new_copyright_text

    # Others

    ## Track Number

    @property
    def track_number(self) -> Optional[Tuple[int, int]]:
        self._logger.warn(
            "Property `track_number` is not supported for %s files", self._extension
        )
        return None

    @track_number.setter
    def track_number(self, new_track_number: Optional[Tuple[int, int]]) -> None:
        self._logger.warn(
            "Property `track_number` is not supported for %s files", self._extension
        )

    ## Disc Number

    @property
    def disc_number(self) -> Optional[Tuple[int, int]]:
        self._logger.warn(
            "Property `disc_number` is not supported for %s files", self._extension
        )
        return None

    @disc_number.setter
    def disc_number(self, new_disc_number: Optional[Tuple[int, int]]) -> None:
        self._logger.warn(
            "Property `disc_number` is not supported for %s files", self._extension
        )

    ## Year

    @property
    def year(self) -> Optional[int]:
        self._logger.warn("Property `year` is not supported for %s files", self._extension)
        return None

    @year.setter
    def year(self, new_year: Optional[int]) -> None:
        self._logger.warn("Property `year` is not supported for %s files", self._extension)

    ## Explicit

    @property
    def explicit(self) -> Optional[bool]:
        self._logger.warn(
            "Property `explicit` is not supported for %s files", self._extension
        )
        return None

    @explicit.setter
    def explicit(self, new_explicit: Optional[bool]) -> None:
        self._logger.warn(
            "Property `explicit` is not supported for %s files", self._extension
        )

    ##Cover

    @property
    def cover_url(self) -> Optional[str]:
        self._logger.warn(
            "Property `cover_url` is not supported for %s files", self._extension
        )
        return None

    @cover_url.setter
    def cover_url(self, new_cover: Optional[str]) -> None:
        self._logger.warn(
            "Property `cover_url` is not supported for %s files", self._extension
        )

    ## Lyrics

    @property
    def lyrics(self) -> Optional[List[str]]:
        self._logger.warn(
            "Property `lyrics` is not supported for %s files", self._extension
        )
        return None

    @lyrics.setter
    def lyrics(self, new_lyrics: Optional[List[str]]) -> None:
        self._logger.warn(
            "Property `lyrics` is not supported for %s files", self._extension
        )

    ## Comments

    @property
    def comments(self) -> Optional[List[str]]:
        self._logger.warn(
            "Property `comments` is not supported for %s files", self._extension
        )
        return None

    @comments.setter
    def comments(self, new_comments: Optional[List[str]]) -> None:
        self._logger.warn(
            "Property `comments` is not supported for %s files", self._extension
        )

    ## Origin website

    @property
    def origin_website(self) -> Optional[List[str]]:
        self._logger.warn(
            "Property `origin_website` is not supported for %s files", self._extension
        )
        return None

    @origin_website.setter
    def origin_website(self, new_origin_website: Optional[List[str]]) -> None:
        self._logger.warn(
            "Property `origin_website` is not supported for %s files", self._extension
        )
