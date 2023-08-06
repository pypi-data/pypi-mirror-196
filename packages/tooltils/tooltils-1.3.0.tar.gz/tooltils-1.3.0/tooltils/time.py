"""
Time modifying and informative functions

### Available Methods:
- epoch() > Return epoch based off system clock
- date() > Convert epoch to human readable date
- sleep() > Block thread execution for specified time in ms
"""


class _bm:
    from datetime import datetime, timezone, timedelta
    from time import time as ctime, localtime, sleep


def epoch() -> float:
    """
    Return epoch based off system clock
    
    >>> epoch()
    float  # Current date as epoch
    """
    
    return _bm.ctime()

def date(epoch: float=epoch(), tz: str='local', format: int=1) -> str:
    """
    Convert epoch to human formatted date
    
    ### Examples:
    >>> date()
    str  # Date in Local Timezone
    >>> date(epoch=0)
    str  # January 1st, 1970
    >>> date(tz='-05:00')
    str # New York, USA
    >>> date(tz='+11:00')
    str # Sydney, Australia
    >>> date(tz='+5555')
    Traceback (most recent call last):
        ...
    TypeError: Timezone not found
    >>> date(epoch=1e100)
    Traceback (most recent call last):
        ...
    OverflowError: Epoch timestamp too large
    """

    try:
        if tz.lower() == 'local':
            sdate = _bm.localtime(epoch)
        elif tz.startswith('+') or tz.startswith('-'):
            try:
                timezone = _bm.timezone(_bm.timedelta(
                           hours=int(tz[:3]), minutes=int(tz[4:])))
                sdate    = _bm.datetime.fromtimestamp(epoch, 
                           tz=timezone).timetuple()
            except (ValueError, IndexError):
                raise TypeError('Timezone not found')
        else:
            raise TypeError('Timezone not found')
    except (OverflowError, TypeError) as err:
        if type(err) is OverflowError:
            raise TypeError('Epoch timestamp too large')
        else:
            raise TypeError('Unable to parse epoch timestamp')

    def fv(val: int) -> str:
        return val if val > 9 else f'0{val}'

    if format == 1:
        return '{}-{}-{} {}:{}:{}'.format(sdate.tm_year,
            fv(sdate.tm_mon), fv(sdate.tm_mday), fv(sdate.tm_hour),
            fv(sdate.tm_min), fv(sdate.tm_sec))

    elif format == 2:
        hour: int = sdate.tm_hour % 12 if sdate.tm_hour % 12 != 0 else 12
        mon: list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                     'August', 'September', 'October', 'November', 'December'][sdate.tm_mon - 1]
        end: list = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th',
                     'th'][int(str(sdate.tm_mday)[-1])]
        if sdate.tm_mday in [11, 12, 13]:
            end: str = 'th'

        return '{}:{} {} on the {}{} of {}, {}'.format(hour, fv(sdate.tm_min), 
               'PM' if sdate.tm_hour >= 12 else 'AM', sdate.tm_mday, end, mon, sdate.tm_year)
    else:
        raise TypeError('Format ({}) not found'.format(format))

def sleep(ms: float) -> None:
    """
    Delay current thread execution for x amount of milliseconds
    
    >>> sleep(1000)
    None  # Execution stops for 1 second
    >>> sleep('hello')
    Traceback (most recent call last):
        ...
    TypeError: Expected type int not 'str'
    """

    if type(ms) is not float:
        raise TypeError('Expected type int not \'{}\''.format(type(ms)))

    _bm.sleep(ms / 1000)
