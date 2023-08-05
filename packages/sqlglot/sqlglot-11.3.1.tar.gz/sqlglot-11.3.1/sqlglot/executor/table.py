from __future__ import annotations

import typing as t

from sqlglot.helper import dict_depth
from sqlglot.schema import AbstractMappingSchema


class Table:
    def __init__(self, columns, rows=None, column_range=None):
        self.columns = tuple(columns)
        self.column_range = column_range
        self.reader = RowReader(self.columns, self.column_range)
        self.rows = rows or []
        if rows:
            assert len(rows[0]) == len(self.columns)
        self.range_reader = RangeReader(self)

    def add_columns(self, *columns: str) -> None:
        self.columns += columns
        if self.column_range:
            self.column_range = range(
                self.column_range.start, self.column_range.stop + len(columns)
            )
        self.reader = RowReader(self.columns, self.column_range)

    def append(self, row):
        assert len(row) == len(self.columns)
        self.rows.append(row)

    def pop(self):
        self.rows.pop()

    @property
    def width(self):
        return len(self.columns)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return TableIter(self)

    def __getitem__(self, index):
        self.reader.row = self.rows[index]
        return self.reader

    def __repr__(self):
        columns = tuple(
            column
            for i, column in enumerate(self.columns)
            if not self.column_range or i in self.column_range
        )
        widths = {column: len(column) for column in columns}
        lines = [" ".join(column for column in columns)]

        for i, row in enumerate(self):
            if i > 10:
                break

            lines.append(
                " ".join(
                    str(row[column]).rjust(widths[column])[0 : widths[column]] for column in columns
                )
            )
        return "\n".join(lines)


class TableIter:
    def __init__(self, table):
        self.table = table
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.table):
            return self.table[self.index]
        raise StopIteration


class RangeReader:
    def __init__(self, table):
        self.table = table
        self.range = range(0)

    def __len__(self):
        return len(self.range)

    def __getitem__(self, column):
        return (self.table[i][column] for i in self.range)


class RowReader:
    def __init__(self, columns, column_range=None):
        self.columns = {
            column: i for i, column in enumerate(columns) if not column_range or i in column_range
        }
        self.row = None

    def __getitem__(self, column):
        return self.row[self.columns[column]]


class Tables(AbstractMappingSchema[Table]):
    pass


def ensure_tables(d: t.Optional[t.Dict]) -> Tables:
    return Tables(_ensure_tables(d))


def _ensure_tables(d: t.Optional[t.Dict]) -> t.Dict:
    if not d:
        return {}

    depth = dict_depth(d)

    if depth > 1:
        return {k: _ensure_tables(v) for k, v in d.items()}

    result = {}
    for name, table in d.items():
        if isinstance(table, Table):
            result[name] = table
        else:
            columns = tuple(table[0]) if table else ()
            rows = [tuple(row[c] for c in columns) for row in table]
            result[name] = Table(columns=columns, rows=rows)

    return result
