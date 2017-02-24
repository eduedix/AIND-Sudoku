import app

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        app.assignments.append(values.copy())
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # pass
    width = 1 + max(len(values[s]) for s in app.boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in app.rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in app.cols))
        if r in 'CF':
            print(line)
    print


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
    return {position: (grid[idx] if grid[idx] != '.' else '123456790') for idx, position in enumerate(cross(app.rows, app.cols))}
