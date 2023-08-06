import sys
from mkdocs_bibtex.plugin import BibTexPlugin

if sys.version_info[:2] >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

__version__ = "2.8.15"
