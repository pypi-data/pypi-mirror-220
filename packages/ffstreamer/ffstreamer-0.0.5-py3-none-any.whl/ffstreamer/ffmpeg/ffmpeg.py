# -*- coding: utf-8 -*-

from os import path
from subprocess import check_output
from typing import Final, List, NamedTuple
from urllib.parse import urlparse

BGR24_CHANNELS: Final[int] = 3
MINIMUM_REALTIME_FRAMES: Final[int] = 12
MEGA_BYTE_UNIT: Final[int] = 1024 * 1024
DEFAULT_BUFFER_SIZE: Final[int] = 100 * MEGA_BYTE_UNIT

# fmt: off
DEFAULT_FFMPEG_INPUT_FORMAT: Final[str] = (
    # global options
    "-hide_banner "
    # infile options
    "-fflags nobuffer -flags low_delay "
    "-i {src} "
    # outfile options
    "-f image2pipe -pix_fmt bgr24 -vcodec rawvideo pipe:1"
)
DEFAULT_FFMPEG_OUTPUT_FORMAT: Final[str] = (
    # global options
    "-hide_banner "
    # infile options
    "-f rawvideo -pix_fmt bgr24 -s {width}x{height} -i pipe:0 "
    # outfile options
    "-c:v libx264 "
    "-preset ultrafast "
    "-crf 30 "
    "-f {format} {dest}"
)
# fmt: on

FFMPEG_PIX_FMTS_HEADER_LINES: Final[int] = 8
"""
Skip unnecessary header lines in `ffmpeg -hide_banner -pix_fmts` command.
Perhaps something like this:

```
Pixel formats:
I.... = Supported Input  format for conversion
.O... = Supported Output format for conversion
..H.. = Hardware accelerated format
...P. = Paletted format
....B = Bitstream format
FLAGS NAME            NB_COMPONENTS BITS_PER_PIXEL
-----
```

For reference, the next line would look something like this:

```
IO... yuv420p                3            12
IO... yuyv422                3            16
IO... rgb24                  3            24
IO... bgr24                  3            24
IO... yuv422p                3            16
IO... yuv444p                3            24
IO... yuv410p                3             9
IO... yuv411p                3            12
IO... gray                   1             8
```
"""


class PixFmt(NamedTuple):
    supported_input_format: bool
    supported_output_format: bool
    hardware_accelerated_format: bool
    paletted_format: bool
    bitstream_format: bool
    name: str
    nb_components: int
    bits_per_pixel: int


def inspect_pix_fmts(ffmpeg_path="ffmpeg") -> List[PixFmt]:
    output = check_output([ffmpeg_path, "-hide_banner", "-pix_fmts"]).decode("utf-8")
    lines = output.splitlines()[FFMPEG_PIX_FMTS_HEADER_LINES:]

    result = list()
    for line in lines:
        cols = [c.strip() for c in line.split()]
        assert len(cols) == 4
        flags = cols[0]
        fmt = PixFmt(
            supported_input_format=(flags[0] == "I"),
            supported_output_format=(flags[1] == "O"),
            hardware_accelerated_format=(flags[2] == "H"),
            paletted_format=(flags[3] == "P"),
            bitstream_format=(flags[4] == "B"),
            name=cols[1],
            nb_components=int(cols[2]),
            bits_per_pixel=int(cols[3]),
        )
        result.append(fmt)
    return result


FFMPEG_FILE_FORMATS_HEADER_LINES: Final[int] = 4
"""
Skip unnecessary header lines in `ffmpeg -hide_banner -formats` command.
Perhaps something like this:

```
File formats:
 D. = Demuxing supported
 .E = Muxing supported
 --
```

For reference, the next line would look something like this:

```
 D  3dostr          3DO STR
  E 3g2             3GP2 (3GPP2 file format)
  E 3gp             3GP (3GPP file format)
 D  4xm             4X Technologies
  E a64             a64 - video for Commodore 64
 D  aa              Audible AA format files
 D  aac             raw ADTS AAC (Advanced Audio Coding)
 D  aax             CRI AAX
 DE ac3             raw AC-3
```
"""


class FileFormat(NamedTuple):
    supported_demuxing: bool
    supported_muxing: bool
    name: str
    description: str


def inspect_file_formats(ffmpeg_path="ffmpeg") -> List[FileFormat]:
    output = check_output([ffmpeg_path, "-hide_banner", "-formats"]).decode("utf-8")
    lines = output.splitlines()[FFMPEG_FILE_FORMATS_HEADER_LINES:]

    result = list()
    for line in lines:
        supported_demuxing = line[1] == "D"
        supported_muxing = line[2] == "E"
        name_desc = line[4:].split(maxsplit=1)
        name = name_desc[0]
        desc = name_desc[1] if len(name_desc) == 2 else str()
        fmt = FileFormat(
            supported_demuxing=supported_demuxing,
            supported_muxing=supported_muxing,
            name=name,
            description=desc,
        )
        result.append(fmt)
    return result


def detect_file_format(url: str, ffmpeg_path="ffmpeg") -> str:
    file_formats = inspect_file_formats(ffmpeg_path)
    o = urlparse(url)

    if o.scheme:
        try:
            file_format = next(filter(lambda f: o.scheme == f.name, file_formats))
        except StopIteration:
            pass
        else:
            return file_format.name

    ext = path.splitext(url)[1]
    return ext[1:] if ext[0] == "." else ext


def calc_recommend_buffer_size(
    width: int,
    height: int,
    channels=BGR24_CHANNELS,
    frames=MINIMUM_REALTIME_FRAMES,
) -> int:
    assert channels >= 1
    assert frames >= 1
    return width * height * channels * frames


def calc_minimum_buffer_size(
    width: int,
    height: int,
    channels=BGR24_CHANNELS,
    frames=MINIMUM_REALTIME_FRAMES,
) -> int:
    recommend_size = calc_recommend_buffer_size(width, height, channels, frames)
    return min(DEFAULT_BUFFER_SIZE, recommend_size)
