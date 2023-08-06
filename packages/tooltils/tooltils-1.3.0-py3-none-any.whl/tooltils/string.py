"""
Custom string modifying methods

### Available Methods:
- cstrip() > Caveman regex replacement
- mreplace() > Replace multiple keywords in a string using a dict
- cipher() > A simple caeser cipher
- halve() > Halve a string and return halves as a list
"""


def cstrip(text: str, chars: str) -> str:
    """Strip a string using a character list as a filter"""

    for i in chars:
        text = text.replace(i, '')

    return text

def mreplace(text: str, chars: dict) -> str:
    """Multi replace words in a string using a dictionary"""

    for i in chars.keys():
        text = text.replace(str(i), str(chars[i]))

    return text

def halve(text: str) -> list:
    """Halve text and return both halves as a list"""

    i: int = len(text)
    if i % 2 == 0:
        return [text[0:i // 2], text[i // 2:]]
    else:
        return [text[0:(i // 2 + 1)], text[(i // 2 + 1):]]

def cipher(text: str, shift: int) -> str:
    """A simple caeser cipher utilising place shifting"""

    for i in text:
        start: int = 65 if i.isupper() else 97
        text += chr((ord(i) + shift - (start)) % 26 + (start))

    return halve(text)[1]
