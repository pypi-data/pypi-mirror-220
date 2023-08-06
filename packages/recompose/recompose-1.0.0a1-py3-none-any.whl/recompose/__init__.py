"""
Recompose is a Python package for templated data recomposition.
"""

from importlib.resources import open_text

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()
