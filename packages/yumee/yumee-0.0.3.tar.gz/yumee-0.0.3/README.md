# Yumee

**Embed metadata into your music files, whatever the type**  
Yumee stands for *Yet Unother MEtadata Embedder*

## Features

- Automatic type detection based on the file extension
    - Currently supported : MP3, M4A, FLAC, OGG (Vorbis), OPUS
- Detection of badly formatted files
- Easy to use, straightforward interface
- Possible to use via DI integration

## Installation

### Pip

```
pip install yumee
```

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

```
poetry add yumee
```

## Usage

There are 2 ways to use this library : using the SongMetadataEmbedder object or via the DI.

### Using SongMetadataEmbedder

The library exposes the SongMetadataEmbedder class. This class has 1 method : `open_file`.

`open_file` opens an audio file at a provided path and returns a `BaseSongFile` to manipulate its metadata.  
Once you have a `BaseSongFile`, you have access to methods like `embed` or `extract`. `embed` modifies the metadata of the SongFile according to the data provided. `extract` returns the metadata that was embedded in the file.

**Example 1 :**

```python
from pathlib import Path
from yumee import SongMetadataEmbedder

embedder = SongMetadataEmbedder()
path = Path("path/to/file.mp3")

with embedder.open_file(path) as song_file:
    song_file.title = "New Title"
```

*It is recommended to use 'open_file' with the 'with' statement as it will ensure that the modifications are saved as you exit the block. Otherwise, you have to make sure to call 'save' to save the modifications.*

**Example 2 :**

```python
from pathlib import Path
from yumee import SongMetadataEmbedder, SongMetadata

embedder = SongMetadataEmbedder()
path = Path("path/to/file.mp3")
metadata = SongMetadata(title="New Title")

song_file = embedder.open_file(path)
song_file.embed(metadata)
```

*The 'embed' method automatically saves the modifications done. This is why I don't use 'open_file' with a 'with' statement.*

### Using DI

The library also exposes a `BaseSongFileProvider` interface and a `add_yumee` function for [Taipan-DI](https://github.com/Billuc/Taipan-DI).

In this function, SongFileProviders are registered as a Pipeline. Each SongFileProvider correspond to a specific file type and generates a `BaseSongFile`. Resolve the pipeline and execute it to have a `BaseSongFile` you can then manipulate.

**Example :**

```python
from yumee import BaseSongFileProvider, add_yumee
from taipan_di import DependencyCollection

services = DependencyCollection()
add_yumee(services)
provider = services.build()

song_file_provider = provider.resolve(BaseSongFileProvider)
path = Path("path/to/file.mp3")

with song_file_provider.exec(path) as song_file:
    ...
```

## Inspirations

This library is partially inspired by spotDL's [spotify-downloader](https://github.com/spotDL/spotify-downloader) and utilises [mutagen](https://mutagen.readthedocs.io/en/latest/).

## TODO

This library isn't stable yet and a lot of things can still be improved.
If there is something you want to see added or if something does not work as you want it to, feel free to open an issue.

Here is a list of features I have in mind and will be working on :

- ~~Generate SongMetadata from a SongFile~~
- Support Wav
- ISRC tag
- MP3 separator support
- Popularity tag (ID3)
