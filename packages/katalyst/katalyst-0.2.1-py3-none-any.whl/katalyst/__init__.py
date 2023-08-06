import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
    __version__ = metadata.version(__package__ or __name__)
else:
    from pkg_resources import get_distribution
    __version__ = get_distribution(__package__ or __name__).version

__version_info__ = tuple(map(int, __version__.split('.')))