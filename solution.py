assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

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


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    def find_naked_twins(values, unit):
        """Find naked twins in a unit
        Args:
            values(dict)
            unit(array)
        Returns:
            array of naked_twins
        """
        from collections import defaultdict

        value_boxes_dict = defaultdict(lambda: [])
        for box in unit:
            if len(values[box]) == 2:
                value_boxes_dict[values[box]].append(box)
        return [value_boxes_dict[value] for value in value_boxes_dict if len(value_boxes_dict[value]) == 2]

    def eliminate_naked_twins_from_unit(values, unit, naked_twins_boxes):
        """Eliminate naked twins value from units
        """
        for box in unit:
            if len(values[box]) > 1 and box not in naked_twins_boxes:
                for naked_twin_value in values[naked_twins_boxes[0]]:
                    assign_value(values, box, values[box].replace(naked_twin_value, ''))

    for unit in unitlist:
        naked_twins_array = find_naked_twins(values, unit)
        if naked_twins_array:
            display(values)
        for naked_twins_boxes in naked_twins_array:
            eliminate_naked_twins_from_unit(
                values, unit, naked_twins_boxes)

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return {position: (grid[idx] if grid[idx] != '.' else '123456789') for idx, position in enumerate(cross(rows, cols))}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # pass
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print


def eliminate(values):
    """
    Eliminate assigned box values from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """
    Assign value to box if only one possible value exists
    """
    for unit in unitlist:
        for digit in cols:
            possible_places = [box for box in unit if digit in values[box]]
            if len(possible_places) == 1:
                assign_value(values, possible_places[0], digit)
    return values


def reduce_puzzle(values):
    """
    Run eliminate and only_choice until the loop stalls.
    Output:
        If a box has 0 possible values False else values grid
    """
    stalled = False
    while not stalled:
        solved_boxes_before = len(
            [box for box in values if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        values = eliminate(values)
        values = only_choice(values)
        solved_boxes_after = len(
            [box for box in values if len(values[box]) == 1])
        stalled = solved_boxes_before == solved_boxes_after
        if len([values[box] for box in values if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
        If values has a box with possible values, do DFS from the box with min(len(possible_values))
    """

    # check if solved already
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in values):
        return values

    # choose box with min possibilities
    possibilities, box = min((len(values[box]), box)
                             for box in boxes if len(values[box]) > 1)

    # use recursion to solve each one of sudoku branches, if one returns a
    # value, return it as answer.
    for possible_value in values[box]:
        new_values = values.copy()
        new_values[box] = possible_value
        attempt = search(new_values)
        if attempt:
            return attempt

    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solved = False

    while not solved:
        attempt = search(values)
        if attempt:
            solved = True
            return attempt


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
