"""
System method wrapper

### Available methods:
- info > Indentifying system information
- exit() > Exit the current thread using an exit code
- clear() > OS independent terminal clearing
- system() > Simplified `subprocess.check_output` wrapper
"""


class _bm:
    from subprocess import call, check_output
    from typing import NoReturn
    from sys import exit

import tooltils.sys.info as info


def exit(_code: int=1, _details: str=None) -> _bm.NoReturn:
    """Exit the current thread using an exit code"""

    if not _details:
        print()
    else:
        print(str(_details))
    _bm.exit(_code)

def clear() -> None:
    """OS independent terminal clearing"""

    if info.platform == 'windows':
        _bm.call(['cls'], shell=True)
    elif info.platform == 'darwin' or info.platform == 'linux':
        _bm.call(['clear'], shell=True)

def system(_args: str='', _shell: bool=True) -> list:
    """Simplified `subprocess.check_output` wrapper"""

    if type(_args) is list or type(_args) is tuple or type(_args) is str:
        data: list = _bm.check_output(args=_args, shell=_shell).decode().splitlines()

    return data
