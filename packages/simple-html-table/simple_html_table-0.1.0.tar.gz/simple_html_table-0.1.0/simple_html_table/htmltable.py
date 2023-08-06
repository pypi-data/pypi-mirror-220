# -*- coding: utf-8 -*-
"""
Module to implement a table that renders to html.

Created on Sat Jun 10 11:24:08 2023

@author: phygbu
"""
from typing import List, Dict, Tuple, Union, Optional

from collections.abc import MutableSequence

import numpy as np


class HTMLObjectMixin(object):

    """Base class that represents an HTML tag entity."""

    def __init__(self, *args: Tuple, **kargs: Dict) -> None:
        """Setup class with list of css classes and other attributes.

        Keyword Arguments:
            tag (str):
                The HTML tag to use.
            classes (list of str):
                A list of css classes to apply. Defaults to html_<tag> where <tag> is the html tag string.
            attrs (dict):
                Dictionary of other html attributes to set.
            content (str):
                The content of the tag if the tag has opening and closing tags. Ignored if the tag is a single tag.
            single_tag (bool):
                Defaults to False. Set True if the tag is a single tag and does not have content between opening and
                closoing tags.

        Methods:
            render(self):
                Render the table to a string of html.
        """
        self.tag: str = kargs.get("tag", "p")
        self._classes: List[str] = kargs.get("classes", [f"html_{self.tag}"]).copy()
        self._attrs: Dict = kargs.get("attrs", {}).copy()
        self._content: str = kargs.get("content", "")
        self._single_tag: bool = kargs.get("single_tag", False)

    def render(self) -> str:
        """Render the current tag to html."""
        classes = f" class='{self.classes}'" if self.classes else ""
        attrs = f" {self.attrs}" if self._attrs else ""
        if not self._single_tag:
            return f"<{self.tag}{classes}{attrs}>{self._content}</{self.tag}>"
        return f"<{self.tag}{classes}{attrs} />"

    @property
    def classes(self) -> Union[str, None]:
        """Return the set of classes for this object as a string or None."""
        if not len(self._classes):
            return None
        return " ".join(self._classes)

    @classes.setter
    def classes(self, value: Union[str, List[str]]) -> None:
        """Set the classes from a string."""
        if isinstance(value, str):
            value = [x.strip() for x in value.split(" ") if x != ""]
        self._classes = [x for x in value if isinstance(x, str) and " " not in x and x != ""]

    @property
    def attrs(self) -> Union[str, None]:
        """Return the object HTML attributes as a string of key=value pairs spearated by spaces."""
        if not len(self._attrs):
            return None
        attrs = []
        for k, v in self._attrs.items():
            if isinstance(v, str):
                v = f"'{v}'"
            attrs.append(f"{k}={v}")
        return " ".join(attrs)

    @attrs.setter
    def attrs(self, value: Union[str, Dict]) -> None:
        self._attrs = {}
        if isinstance(value, str):
            for attr in value.split(" "):
                parts = attr.split("=")
                key = parts[0]
                val = "=".join(parts[1:]).strip().strip("'\"")
                for typ in [float, int, bool, str]:
                    try:
                        val = typ(val)
                        break
                    except (ValueError, TypeError):
                        pass
                self._attrs[key] = val
        else:
            for k, v in value:
                self._attrs[k] = v

    @property
    def attrs_dict(self) -> Dict[str, str]:
        """Return the HTML atriobutes as a dictionary."""
        return self._attrs

    @property
    def classes_list(self) -> List[str]:
        """Return the HTML classes as a list of strings."""
        return self._classes


class Table(HTMLObjectMixin, MutableSequence):

    """Represents an HTML table as a sequence of rows, or a 2D array.

    Attributes:
        classes (str):
            Represents the css classes of the table as a space separated string.
        classes_list (list of str):
            Returns the css classes as a mutable list
        attrs (str):
            Returns the html attributes of the table as a space spearated string of attr=value pairs.
            When setting the attrs, you can also pass it a dictionary
        attrs_dict (dict):
            Represents the attributes of the Table as a mutable dictionary.

    Methods:
        render(self):
            Render the table to a string of html.
    """

    def __init__(self, size: Tuple[int, int], **kargs: Dict) -> None:
        """Initialise the html Table object.

        Arguments:
            size (tuple of int,int ):
                Size of the table (rows x columns) to create.

        Keyword Arguments:
            tag (str):
                The HTML tag to use - defaults to TABLE.
            classes (list of str):
                A list of css classes to apply. Defaults to html_<tag> where <tag> is the html tag string.
            attrs (dict):
                Dictionary of other html attributes to set.
            table_contents (2D numpy array of str or callable):
                Cell contents - must be the same shap as the size argument.
            row_classes (list of str):
                As classes, but applied to each row
            row_attrs (dict):
                As attrs, but applied to each row
            cell_classes (list of str):
                As classes but applied to each cell
            cell_attrs(dict):
                As attrs, but applies to each cell.
        """
        kargs.setdefault("tag", "table")
        table_contents = kargs.pop("table_contents", np.zeros(size, dtype=str))
        if not callable(table_contents) and table_contents.shape != size:
            raise ValueError(f" Table size {size} and table_contents shape {table_contents.shape} not the same!")
        for remove in ["content", "single_tag"]:  # Suppress HTMLObject arguments we don't want.
            kargs.pop(remove, None)
        super().__init__(**kargs)
        for no_pass in ["classes", "attrs", "tag"]:
            kargs.pop(no_pass, None)
        row_classes = kargs.pop("row_classes", ["html_tr"])
        row_attrs = kargs.pop("row_attrs", {})
        rows, cols = size
        self._rows = [
            Row(cols, row=ix, table=self, classes=row_classes, attrs=row_attrs, table_contents=table_contents, **kargs)
            for ix in range(rows)
        ]

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, item: Union[Tuple[int, int], int]) -> Union["Cell", "Row"]:
        if isinstance(item, tuple):
            r, c = item
            return self._rows[r][c]
        return self._rows[item]

    def __setitem__(self, item: Union[Tuple[int, int], int], val: Union["Cell", "Row", "str"]) -> None:
        if isinstance(item, tuple) and isinstance(val, Cell):
            r, c = item
            self._rows[r][c] = val
        elif isinstance(item, tuple) and isinstance(val, str):
            r, c = item
            self._rows[r][c]._content = val
        elif isinstance(item, int) and isinstance(val, Row) and len(val) == len(self._rows[0]):
            for ix, cell in enumerate(val):
                self._rows[item][ix] = cell
        else:
            raise NotImplementedError(f"Unable to set item for {item=} {val=}")

    def __delitem__(self, item: int) -> None:
        raise NotImplementedError("Unable to delete specific rows from the table")

    def insert(self, item: int, value: "Cell") -> None:
        raise NotImplementedError("Unable to resize an HTML table after it is created")

    def render(self) -> str:
        """Build self._content based on the cells defined."""
        content = ""
        for ix, row in enumerate(self._rows):
            content += row.render()
        if len(content) == 3:
            content = ""
        self._content = "\n" + content
        return super().render()


class Row(HTMLObjectMixin, MutableSequence):

    """Represents a single row in an HTML Table as a mutable sequence.

    Attributes:

        location (int):
            Returns the integer index of this row within its Table.
        header (list of bool):
            Read or set whether the cells in this row are headers or not.
        classes (str):
            Represents the css classes of the row  as a space separated string.
        classes_list (list of str):
            Returns the css classes as a mutable list
        attrs (str):
            Returns the html attributes of the row as a space spearated string of attr=value pairs.
            When setting the attrs, you can also pass it a dictionary
        attrs_dict (dict):
            Represents the attributes of the row as a mutable dictionary.

    Methods:
        render(self):
            Render the table to a string of html.
    """

    def __init__(self, size: int, row: int = 0, table: Optional[Table] = None, **kargs: Dict):
        """Initialise the row object by storing a sequence of cells and a link to a parent table."""
        kargs.setdefault("tag", "tr")
        super().__init__(**kargs)
        for no_pass in ["content", "classes", "attrs", "tag"]:
            kargs.pop(no_pass, None)
        cell_classes = kargs.pop("cell_classes", ["html_td"])
        cell_attrs = kargs.pop("cell_attrs", {})
        cols = size
        self._row = row
        self._table = table
        table_contents = kargs.get("table_contents")
        self._cols = []
        for ix in range(cols):
            if callable(table_contents):
                content = table_contents
            else:
                content = table_contents[row, ix]
            self._cols.append(Cell(ix, self, table, classes=cell_classes, attrs=cell_attrs, content=content))

    @property
    def location(self) -> int:
        """Integer index of the current row."""
        return self._row

    @property
    def header(self) -> List[bool]:
        """Are the cells in this row header cells?"""
        return [c.header for c in self]

    @header.setter
    def header(self, value: Union[bool, List[bool]]) -> None:
        """Set whether the cells in this row are header cells."""
        if isinstance(value, bool):
            value = [value] * len(self)
        for c, v in zip(self, value):
            c.header = v

    def __len__(self):
        return len(self._cols)

    def __getitem__(self, item: int) -> "Cell":
        return self._cols[item]

    def __setitem__(self, item: int, value: "Cell") -> None:
        if not 0 <= item < len(self):
            raise IndexError(f"{item} is out of bounds")
        current = self[item]
        value._table = self._table
        value._row = self
        value._col = item
        self._cols[item] = value

    def __delitem__(self, item: int) -> None:
        raise NotImplementedError("Unable to delete specific cells from the table")

    def insert(self, item: int, value: "Cell") -> None:
        raise NotImplementedError("Unable to resize an HTML table after it is created")

    def render(self) -> str:
        """Build self._content based on the cells defined."""
        content = ""
        for ix, cell in enumerate(self._cols):
            if cell.location == (self._row, ix):  # Only oputput cell if it's located here
                content += "\n\t\t" + cell.render()
        self._content = content + "\n\t"
        return "\t" + super().render() + "\n"


class Cell(HTMLObjectMixin):

    """Represent a single HTML cell in  a table.

    Attributes:
        location (tuple[int,int]):
            Index location of the cell within its HTML table.
        size (tuple[int,int]):
            The number of rows and columns spanned by this cell.
        header (bool):
            If True, render the cell with th tags, otherwise with td tags.
        rowspan, colspan (int):
            Set the number or rows or columns spanned by the current cell.
        tag (str):
            The HTML tag for this element - usually either a td or th.
        classes (str):
            Represents the css classes of the cell as a space separated string.
        classes_list (list of str):
            Returns the css classes as a mutable list
        attrs (str):
            Returns the html attributes of the cell as a space spearated string of attr=value pairs.
            When setting the attrs, you can also pass it a dictionary
        attrs_dict (dict):
            Represents the attributes of the cell as a mutable dictionary.
        content (str or callable):
            The contents of the cell. If callable, then expects a function that takes the cell as its single argument.

    """

    def __init__(self, col: int, row: Row, table: Table, **kargs):
        """Initialise the cell."""
        self._table = table
        self._row = row
        self._col = col
        kargs.setdefault("tag", "td")
        self._rspan = kargs.pop("rowspan", kargs.get("attrs", {}).get("rowspan", 1))
        self._cspan = kargs.pop("colspan", kargs.get("attrs", {}).get("colspan", 1))
        if callable(kargs.get("content", "")):
            kargs["content"] = kargs["content"](self)
        super().__init__(**kargs)
        if self._rspan > 1:
            self._attrs["rowspan"] = self._rspan
        if self._cspan > 1:
            self._attrs["colspan"] = self._cspan

    @property
    def location(self) -> Tuple[int, int]:
        """Get the current location of this cell within its table."""
        return self._row.location, self._col

    @property
    def size(self) -> Tuple[int, int]:
        """Get the current rowspan and columnspan of the cell."""
        return self._rspan, self.colspan

    @size.setter
    def size(self, value: Tuple[int, int]) -> None:
        """Set rowspan and columnspan on the current cell."""
        self.rowspan, self.colspan = value

    @property
    def header(self) -> bool:
        """Get whether this cell is a header cell or not."""
        return self.tag == "th"

    @header.setter
    def header(self, val: bool) -> None:
        """Set whether this cell is a header cell or not."""
        self.tag = "th" if val else "td"

    @property
    def rowspan(self) -> int:
        """Get the number of rows spaned by this cell."""
        return self._rspan

    @rowspan.setter
    def rowspan(self, value: int):
        """Set the number of rows spanned by this cell and then adjust the other cells in the table to match."""
        if value == self._rspan:  # NOP
            return
        rl, cl = self.location
        rs, cs = self.size

        if value > rs:  # Expanding the current rowspan
            for c in range(cl, cl + cs):  # iterate over all columns
                for r in range(rl + rs, rl + value):
                    self._table[r]._cols[c] = self  # Overwrite cell with a copy of self
        else:
            for c in range(cl, cl + cs):  # iterate over all columns
                for r in range(rl + value, rl + rs):
                    self._table[r]._cols[c] = Cell(c, self._table[r], self._table, contents="")
        self._attrs["rowspan"] = value
        self._rspan = value

    @property
    def colspan(self) -> int:
        """Get the number of columns spanned by this cell."""
        return self._cspan

    @colspan.setter
    def colspan(self, value: int):
        """Set the number of columns spanned by this cell and adjust the other cells in the table to match."""
        if value == self._cspan:  # NOP
            return
        rl, cl = self.location
        rs, cs = self.size
        if value > cs:  # increasing rows of this instance
            for r in range(rl, rl + rs):  # Iterate over all rows
                for c in range(cl + cs, cl + value):
                    self._table[r]._cols[c] = self
        else:
            for r in range(rl, rl + rs):
                for c in range(cl + value, cl + cs):
                    self._table[r]._cols[c] = Cell(c, self._table[r], self._table, contents="")
        self._attrs["colspan"] = value
        self._cspan = value


if __name__ == "__main__":

    contents = [
        ["Head 1", "Head 2", "Head 3", "Head 4"],
        ["(1,1)", "(1,2)", "(1,3)", "(1,4)"],
        ["(2,1)", "(2,2)", "(2,3)", "(2,4)"],
    ]

    table = Table((3, 4), table_contents=np.array(contents))

    table[1, 1].colspan = 2
    table[0, 0].rowspan = 3
    table[0, 1].attrs_dict.update({"style": "{ background: red; }"})
    table[0].header = True
    for cell in table[0]:
        cell.classes = "table_th"

    result = table.render()
    print(result,"\n")

    def content_func(cell: Cell) -> str:
        """Callback function to fill in the table."""
        row, col = cell.location
        return contents[row][col]

    table2 = Table((3, 4), table_contents=content_func)
    result = table2.render()
    print(result)
