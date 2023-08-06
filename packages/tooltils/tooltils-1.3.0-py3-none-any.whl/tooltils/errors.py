"""
General errors used for better information use

### Available Errors:
- JSONDecoderError > Unable to parse JSON data
"""


class JSONDecoderError(TypeError):
    """Unable to decode JSON input"""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return 'Unable to decode JSON'
