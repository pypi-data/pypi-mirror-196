"""
Terminal modifiers

### Available Methods:
- colours > List of supported terminal colours and corresponding values
- ctext() > Return text in the specified colour
- log() > Log text to the terminal
"""


class _bm:
    from .sys import system
    from .time import date


colours: dict = {'pink': '35', 'green': '32', 'blue': '34', 
                 'yellow' : '33', "red": "31", "white": "38",
                 "cyan": "36", "gray": "0"}

def ctext(text: str='', colour: str='white', bold: bool=False) -> str:
    """Return text in specified colour"""

    try:
        cvalue = colours[colour]
    except ValueError:
        cvalue = colour

    _bm.system('')
    return '\u001b[{0}{1}{2}\u001b[0m'.format(cvalue, ';1m' if bold else 'm', text)

def log(header: str, details: str, type: int=0) -> None:
    """Log text to the terminal as an info, warning or error type"""

    try:
        data = [[ctext('INFO', 'blue', True), '     '],
                [ctext('WARNING', 'yellow', True), '  '],
                [ctext('ERROR', 'red', True), '    ']][type]
    except IndexError:
        raise IndexError('Unknown type \'{}\''.format(type))

    _bm.system('')
    print('{0} {1}{2}{3} {4}'.format(ctext(_bm.date(), 'gray', True), data[0], data[1],
                                     ctext(header, 'pink'), details))
