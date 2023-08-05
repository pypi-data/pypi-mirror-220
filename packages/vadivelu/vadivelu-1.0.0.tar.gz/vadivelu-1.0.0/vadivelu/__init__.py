"""
The MIT License (MIT)

Copyright (c) 2023-present TheMaster3558

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from typing_extensions import Final


__version__: Final[str] = '1.0.0'
__title__ = 'vadivelu'
__author__ = 'TheMaster3558'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023-present TheMaster3558'

__all__: Tuple[str, ...] = ('available_formats', 'get_available_formats', 'pick_available_format', 'get_media_url')


gif_only = ('gif',)
jpg_only = ('jpg',)
both = gif_only + jpg_only


available_formats: Dict[int, Tuple[str, ...]] = {
    100: both,
    101: both,
    200: both,
    201: jpg_only,
    206: both,
    301: jpg_only,
    302: jpg_only,
    307: jpg_only,
    400: both,
    401: jpg_only,
    402: jpg_only,
    403: jpg_only,
    404: both,
    405: jpg_only,
    406: jpg_only,
    408: jpg_only,
    409: jpg_only,
    410: both,
    411: jpg_only,
    412: jpg_only,
    417: jpg_only,
    421: gif_only,
    422: jpg_only,
    423: both,
    424: gif_only,
    499: gif_only,
    500: both,
    502: jpg_only,
    506: jpg_only,
    508: jpg_only,
}


def get_available_formats(code: int) -> Tuple[str, ...]:
    if code not in available_formats:
        raise ValueError(
            f'That code is not valid, valid codes are {", ".join(map(str, available_formats))}'
        )
    return available_formats[code]


def pick_available_format(code: int, priority: str = 'gif') -> str:
    if priority == 'gif':
        return get_available_formats(code)[0]
    elif priority == 'jpg':
        return get_available_formats(code)[-1]
    else:
        raise ValueError('Priority must be jpg or gif')


def get_media_url(code: int, media_format: str) -> str:
    if media_format not in get_available_formats(code):
        raise ValueError(
            f'Media format {media_format} not available for {code}, available formats are {", ".join(available_formats[code])}'
        )

    return f'https://vadivelu.anoram.com/{media_format}/{code}'
