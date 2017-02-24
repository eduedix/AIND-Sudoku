assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

from utils import cross, assign_value, display, grid_values
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
diagonal_units = [[''.join(box) for box in list(zip(rows, cols))], [
    ''.join(box) for box in list(zip(reversed(rows), cols))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)