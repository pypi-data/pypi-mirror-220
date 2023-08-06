# -*- coding: utf-8 -*-
"""
A simple_html_table is a very simple library for making html tables.

The raison d'etre for the package is to allow tables where cells have rowspan and colspan attributes set as well
as allowing per-table, per-row and per-cell arbitary attributes.
"""
__all__ = ["Table", "Row", "Cell"]

__version_info__ = (0, 1, 0)
__version__ = ".".join([str(x) for x in __version_info__])
__author__ = "Gavin Burnell <https://github.com/gb119>"

from .htmltable import Table, Row, Cell
