"""
Custom WAVE file methods

### Available Methods:
- length() > Get the length of a wave file in seconds
"""


class _bm:
    from io import TextIOWrapper
    from os.path import getsize


def length(_file: _bm.TextIOWrapper | str) -> float:
    """Return the length of a wave file in seconds"""

    _file: str = _file.name if type(_file) is _bm.TextIOWrapper else _file
    with open(_file, encoding='latin-1') as _f:
        _f.seek(28)
        sdata: str = _f.read(4)
    rate: int = 0
    for i in range(4):
        rate += ord(sdata[i]) * pow(256, i)

    return round((_bm.getsize(_file) - 44) * 1000 / rate / 1000, 2)
