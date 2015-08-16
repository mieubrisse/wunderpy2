'''
Defines exceptions that can be raised by the Wunderlist client
'''

class _WunderlistError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return str(self.msg)

class ConnectionError(_WunderlistError):
    pass

class TimeoutError(_WunderlistError):
    pass

# TODO Add exceptions for bad request and not found
