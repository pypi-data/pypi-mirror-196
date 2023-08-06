"""
Custom file method wrapper
 
### Available Methods:
- clear() > Clear a file while avoiding null character error
"""


class _bm:
    from io import TextIOWrapper, UnsupportedOperation


def clear(file: _bm.TextIOWrapper) -> None:
    """Clear a file using truncate"""

    if type(file) is not _bm.TextIOWrapper:
        raise TypeError('Expected type TextIOWrapper but received \'{}\''.format(type(file)))
    elif 'r' in file.mode and file.mode != 'r+':
        raise _bm.UnsupportedOperation('Cannot write to file from mode \'{}\''.format(file.mode))
    try:
        file.seek(0)
        file.truncate(0)
    except ValueError:
        raise _bm.UnsupportedOperation('File has been closed')
