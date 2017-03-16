from app import assign_value, display, unitlist, peers, cols, boxes, grid_values, assignments
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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

        # Create a dict with {value: [box]}
        value_boxes_dict = defaultdict(lambda: [])
        for box in unit:
            if len(values[box]) == 2:
                value_boxes_dict[values[box]].append(box)
        # Return [box if len(dict[value]) == 2]
        return [value_boxes_dict[value] for value in value_boxes_dict if len(value_boxes_dict[value]) == 2]

    def eliminate_naked_twins_from_unit(values, unit, naked_twins_boxes):
        """Eliminate naked twins value from units
        """
        for box in unit:
            if len(values[box]) > 1 and box not in naked_twins_boxes:
                for naked_twin_value in values[naked_twins_boxes[0]]:
                    assign_value(values, box, values[box].replace(naked_twin_value, ''))

    # Find naked twins in the units and eliminate them from the unit
    for unit in unitlist:
        naked_twins_array = find_naked_twins(values, unit)
        for naked_twins_boxes in naked_twins_array:
            eliminate_naked_twins_from_unit(
                values, unit, naked_twins_boxes)

    return values

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
