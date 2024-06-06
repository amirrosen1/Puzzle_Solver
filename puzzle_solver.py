#############################################################
# FILE: puzzle_solver.py
# WRITER: Amir Rosengarten, amir.rosen15, 207942285
# EXERCISE: intro2cs2 ex8 2022
# DESCRIPTION:In this exercise we will represent a logic puzzle (game),
# and we will use Backtracking to solve it.
#############################################################


from typing import List, Tuple, Set, Optional, Union, Any

# We define the types of a partial picture and a constraint
# (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    The function gets a partial image and a location on top of it, and
     returns the number of cells visible from the cell at that location
      if all the unknown cells are considered white.
    :param picture: A two-dimensional list representing a partial image.
    :param row: An integer representing an index of a row in the partial
     image.
    :param col: An integer representing an index of a column in the
     partial image.
    """

    val = picture[row][col]
    if val == 0:
        return 0
    count = 1
    # Go over the part that is above the val.
    up = row - 1
    while up >= 0 and picture[up][col] != 0:
        up -= 1
        count += 1
    # Go over the part that is below the val.
    down = row + 1
    while down < len(picture) and picture[down][col] != 0:
        down += 1
        count += 1
    # Go over the part to the right of the val.
    right = col + 1
    while right < len(picture[0]) and picture[row][right] != 0:
        right += 1
        count += 1
    # Go over the part to the left of the val.
    left = col - 1
    while left >= 0 and picture[row][left] != 0:
        left -= 1
        count += 1
    return count


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    The function gets a partial image and a location on top of it, and
     returns the number of cells visible from the cell at that location
      if all the unknown cells are considered black.
    :param picture: A two-dimensional list representing a partial image.
    :param row: An integer representing an index of a row in the partial
     image.
    :param col: An integer representing an index of a column in the
     partial image.
    """

    val = picture[row][col]
    if val == 0 or val == -1:
        return 0
    count = 1
    # Go over the part that is above the val.
    up = row - 1
    while up >= 0 and picture[up][col] == 1:
        up -= 1
        count += 1
    # Go over the part that is below the val.
    down = row + 1
    while down < len(picture) and picture[down][col] == 1:
        down += 1
        count += 1
    # Go over the part to the right of the val.
    right = col + 1
    while right < len(picture[0]) and picture[row][right] == 1:
        right += 1
        count += 1
    # Go over the part to the left of the val.
    left = col - 1
    while left >= 0 and picture[row][left] == 1:
        left -= 1
        count += 1
    return count


def check_lst(possible_vals: List[int]) -> int:
    """
    The function gets a list of numbers (0,1,2), which represent the
     constraint level of constraint in the constraint list. The function
      checks according to the requirements of the exercise what value it
       should return, and it returns it.
    :param possible_vals: List of integers.
    """

    # If the list has 0, the function returns 0. If the whole list has
    # only the value 1, the function returns 1. Otherwise, it returns 2.
    if 0 in possible_vals:
        return 0
    flag = True
    for i in range(len(possible_vals)):
        if possible_vals[i] != 1:
            flag = False
    if flag:
        return 1
    else:
        return 2


def check_constraints(picture: Picture,
                      constraints_set: Set[Constraint]) -> int:
    """
    The function receives a partial image and a list of constraints,
     and returns an integer between 0 and 2 that indicates the success in
      satisfying the constraints in the partial image.
      0 = If at least one of the constraints is breached.
      1 = If all the constraints are met exactly.
      2 = If a certain constraint may exist.
    :param picture: A two-dimensional list representing a partial image.
    :param constraints_set: The constraint group.
    """

    possible_vals = list()
    for con in constraints_set:
        row_id, col_id, val_id = con[0], con[1], con[2]
        # Call the functions max_seen_cells, min_seen_cells.
        max_val = max_seen_cells(picture, row_id, col_id)
        min_val = min_seen_cells(picture, row_id, col_id)
        if val_id > max_val or val_id < min_val:
            possible_vals.append(0)
        elif val_id == min_val and val_id == max_val:
            possible_vals.append(1)
        else:
            possible_vals.append(2)
    # Call the function check_lst.
    finale_val = check_lst(possible_vals)
    return finale_val


def help_solve_puzzle(picture: Picture, constraints_set: Set[Constraint],
                      index_row=0, index_col=0) -> Optional[Picture]:

    """
    The function gets a list of constraints and the game board and two
     variables (initialized to 0). The function checks if there is any
      solution. If it exists, the function returns one solution of the
       board, otherwise it returns None.
    :param picture: A two-dimensional list representing a partial image.
    :param constraints_set: The constraint group.
    :param index_row: The index of the row.
    :param index_col: The index of the columns.
    """

    # Call the function check_constraints. If the function returns 0, then
    # there is no solution at all for the constraint group.
    if check_constraints(picture, constraints_set) == 0:
        return None
    # Base case: If the index of the rows is greater than or equal to the
    # length of the image, then we return the image.
    if index_row >= len(picture):
        return picture
    if picture[index_row][index_col] != -1:
        if index_col == len(picture[0]) - 1:
            # Iterate over cells in columns. If we have finished checking
            # for a particular row, move on to the next row, and if not,
            # then move on to the next column.
            return help_solve_puzzle(picture, constraints_set,
                                     index_row + 1, 0)
        return help_solve_puzzle(picture, constraints_set, index_row,
                                 index_col + 1)
    # Initialize the value at a certain position to 1, and check if this
    # placement is possible.
    picture[index_row][index_col] = 1
    if index_col == len(picture[0]) - 1:
        val_1 = help_solve_puzzle(picture, constraints_set, index_row + 1,
                                  0)
    else:
        val_1 = help_solve_puzzle(picture, constraints_set, index_row,
                                  index_col + 1)
    # If the placement was successful, then the solution of the board is
    # returned.
    if val_1 is not None:
        return val_1
    # Initialize the value at a certain position to 0, and check if this
    # placement is possible.
    picture[index_row][index_col] = 0
    if index_col == len(picture[0]) - 1:
        val_2 = help_solve_puzzle(picture, constraints_set, index_row + 1,
                                  0)
    else:
        val_2 = help_solve_puzzle(picture, constraints_set, index_row,
                                  index_col + 1)
    # If the placement was successful, then the solution of the board is
    # returned.
    if val_2 is not None:
        return val_2
    picture[index_row][index_col] = -1
    return None


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> \
        Optional[Picture]:

    """
    The function receives a set of constraints and a table size, and
     returns an image describing one solution of the board, if any.
    :param constraints_set: The constraint group.
    :param n: The number of lines in the game board.
    :param m: The number of columns in the game board.
    """

    # Create the game board according to the desired sizes, and initialize
    # each value in it to -1.
    picture = [[-1] * m for _ in range(n)]
    # The following lines run on the list of constraints and check if the
    # number that appears on the board is 1 or 0, and change the board
    # accordingly.
    for i in constraints_set:
        if i[2] == 0:
            picture[i[0]][i[1]] = 0
        else:
            picture[i[0]][i[1]] = 1
    # Call the function help_solve_puzzle.
    finale = help_solve_puzzle(picture, constraints_set)
    return finale


def helper_count_solutions(picture: Picture,
                           constraints_set: Set[Constraint],
                           row=0, col=0) -> int:

    """
    The function gets the game board, list of constraints, and 2 variables
     (initialized to 0). The function checks if there is a solution to the
      board considering the list of constraints. If there is a function
       summed some solutions have a total, if there is no function
        returns 0.
    :param picture: A two-dimensional list representing the game board.
    :param constraints_set: The constraint group.
    :param row: The number of lines in the game board.
    :param col: The number of columns in the game board.
    """

    # Call the function check_constraints. If the function returns 0, then
    # there is no solution at all for the constraint group.
    if check_constraints(picture, constraints_set) == 0:
        return 0
    # Base case: If the index of the rows is greater than or equal to the
    # length of the image, then we have finished going over the board, and
    # we have a solution, so we'll return 1.
    if row >= len(picture):
        return 1
    if picture[row][col] == -1:
        # Initialize the variable to 0 for the location, and check if
        # there is a solution for this placement.
        picture[row][col] = 0
        # Iterate over cells in columns. If we have finished checking
        # for a particular row, move on to the next row, and if not,
        # then move on to the next column.
        if col >= len(picture[0])-1:
            val = helper_count_solutions(picture, constraints_set, row + 1,
                                         0)
        else:
            val = helper_count_solutions(picture, constraints_set, row,
                                         col + 1)
        # Initialize the variable to 1 for the location, and check if
        # there is a solution for this placement.
        picture[row][col] = 1
        if col >= len(picture[0]) - 1:
            val_1 = helper_count_solutions(picture, constraints_set,
                                           row + 1, 0)
        else:
            val_1 = helper_count_solutions(picture, constraints_set, row,
                                           col + 1)
        picture[row][col] = -1
        # The sum of the solutions.
        return val + val_1
    # Checking whether we have finished going through the columns of the
    # board and summoning the recursive operation in order to go through
    # a row / column.
    if col >= len(picture[0]) - 1:
        return helper_count_solutions(picture, constraints_set, row + 1, 0)
    else:
        return helper_count_solutions(picture, constraints_set, row,
                                      col + 1)


def how_many_solutions(constraints_set: Set[Constraint], n: int,
                       m: int) -> int:

    """
    The function receives a set of constraints and a table size (number of
     rows and number of columns) that represents a game board, and returns
      the number of different solutions that this board has.
    :param constraints_set: The constraint group.
    :param n: The number of lines in the game board.
    :param m: The number of columns in the game board.
    """

    # Create the game board according to the desired sizes, and initialize
    # each value in it to -1.
    picture = [[-1] * m for _ in range(n)]
    # The following lines run on the list of constraints and check if the
    # number that appears on the board is 1 or 0, and change the board
    # accordingly.
    for i in constraints_set:
        if i[2] == 0:
            picture[i[0]][i[1]] = 0
        else:
            picture[i[0]][i[1]] = 1
    # Call the function help_count_solutions.
    count = helper_count_solutions(picture, constraints_set)
    return count


def help_generate_puzzle(s_constraint: Set[Constraint], n: int, m: int) \
        -> Union[bool, Set[Constraint]]:

    """
    The function gets the general list of constraints of the game board,
     the number of rows, and the number of columns of the board.
      The function checks what is the necessary set of constraints for
       solving the game and returns it.
    :param s_constraint: The constraint group.
    :param n: The number of lines in the game board.
    :param m: The number of columns in the game board.
    """

    # Call the function count_solutions.
    count_solutions = how_many_solutions(s_constraint, n, m)
    # Check if there is a single solution for the board or not.
    if count_solutions > 1:
        return False
    # In the following lines we run on the list of constraints, and each
    # time we take out a certain constraint and recursively check whether
    # that constraint is necessary or not.
    for constrain in s_constraint:
        s_constraint.remove(constrain)
        result = help_generate_puzzle(s_constraint, n, m)
        if result:
            return result
        s_constraint.add(constrain)
    return s_constraint


def generate_puzzle(picture: Picture) -> Set[Constraint]:

    """
    The function takes a picture and returns a set of constraints which
     describes a solution to the board, which this solution is single,
      and all the numbers which are written on the board are necessary for
       its solution.
    :param picture: A two-dimensional list representing the game board.
    """

    # Define the list of constraints.
    s_constraint = set()
    row = len(picture)
    col = len(picture[0])
    # In the following lines we examine all the possible constraints to
    # the game board, and add each constraint to the list of constraints.
    for rows in range(len(picture)):
        for cols in range(len(picture[0])):
            # Call the function min_seen_cells.
            count = min_seen_cells(picture, rows, cols)
            s_constraint.add((rows, cols, count))
    # Call the function help_generate_puzzle.
    return help_generate_puzzle(s_constraint, row, col)
