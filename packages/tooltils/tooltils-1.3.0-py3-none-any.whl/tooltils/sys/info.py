"""
Identifying system information

### Available variables:
- pyv > Python version
- pyv_tuple > Python version as a tuple
- platform > Current OS
- pinfo > OS version
- cpu > CPU name
- name > Computer name
- bitsize > 64-bitness of OS
    
Note: Python 3.10+ required for Linux platform version
"""


class _bm:
    from platform import (system, machine, win32_ver, 
                          mac_ver, python_version_tuple,
                          node)
    if int(python_version_tuple()[1]) > 9:
        from platform import freedesktop_os_release
    from sys import maxsize


pyv:         str = '.'.join(_bm.python_version_tuple())
pyv_tuple: tuple = tuple([int(i) for i in _bm.python_version_tuple()])
platform:    str = _bm.system().lower()

if platform == 'windows':
    pinfo: str = _bm.win32_ver()[0]
elif platform == 'darwin':
    pinfo: str = _bm.mac_ver()[0]
elif platform == 'linux':
    if pyv_tuple[1] > 9:
        pinfo: str = _bm.freedesktop_os_release()
    else:
        pinfo      = None

cpu:     str = _bm.machine().lower()
name:    str = _bm.node()
bitsize: str = '64bit' if _bm.maxsize > 2 ** 32 else '32bit'
