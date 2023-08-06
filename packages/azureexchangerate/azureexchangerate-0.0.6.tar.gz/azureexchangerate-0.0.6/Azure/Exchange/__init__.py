from _rates import rates
from _version import VERSION

__version__ = VERSION

def rate()->list:
    return rates()

__all__ = [
    'rates'
]


