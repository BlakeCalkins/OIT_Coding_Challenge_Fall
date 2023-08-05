import random


def make_grid():
    # This function makes the initial grid of periods. It will be modified later
    # according to the inputs of the player and computer.
    grid = []
    for r in range(3):
        grid.append([])
        for c in range(3):
            grid[r].append('.')
    return grid


def print_grid(grid):
    # Prints out the grid to the terminal.
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            print(grid[r][c], end=' ')
        print()


def mark_grid(grid, tuple_coords, value):
    # takes coordinates (as a tuple, unpacking them first) and changes the grid at
    # them to show the given value.
    inrow, incolumn = tuple_coords
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if row == inrow and column == incolumn:
                grid[row][column] = value
    return grid


def has_three_down_left(grid, value):
    # Checks if the down left diagonal on the grid are all the same value.
    for r, c in zip(range(3), range(2, -1, -1)):
        if grid[r][c] != value:
            return False
    return True


def has_three_right(grid, value):
    # Checks if any row has three in a row of the same value.
    for r in range(3):
        if grid[r][0] != value:
            continue
        values = 0
        for c in range(3):
            if grid[r][c] == value:
                values += 1
            if values == 3:
                return True
    return False


def has_three_down_right(grid, value):
    # Checks if the down right diagonal on the grid are all the same value.
    for r, c in zip(range(3), range(3)):
        if grid[r][c] != value:
            return False
    return True


def has_three_down(grid, value):
    # Checks if any column has three in a row of the same value.
    for c in range(3):
        num_values = 0
        for r in range(3):
            if grid[r][c] == value:
                num_values += 1
            if num_values == 3:
                return True
    return False


def someone_won(grid, value):
    # Checks for three in a row in any direction on the grid of the given value.
    if has_three_down_right(grid, value) \
            or has_three_down_left(grid, value) \
            or has_three_down(grid, value) \
            or has_three_right(grid, value):
        return True
    return False


def get_coords():
    # Gets coordinates from the player character. The coordinates are checked to see
    # if they are inputted correctly and within the grid range of 2.
    while True:
        coords = input("Enter coordinates (two numbers between 0 and 2, separated by a comma. Example 0, 1): ")
        try:
            coords = coords.split(',')
            num1 = int(coords[0])
            num2 = int(coords[1])
            if num1 < 0 or num2 < 0 or num1 > 2 or num2 > 2:
                print('Invalid coordinates. Please choose between 0 and 2.')
                continue
            return num1, num2
        except ValueError:
            print('Please input coordinates as two numbers, separated by a comma.')


def coords_occupied(grid, tuple_coords):
    # Checks if given coordinates on the grid are already occupied with an 'X' or 'O'
    inrow, incolumn = tuple_coords
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if row == inrow and column == incolumn:
                if grid[row][column] != '.':
                    return True
    return False


def computer_coords(grid):
    # Has the computer select two random coordinates. if the coordinates are occupied,
    # the computer selects again until it finds an unoccupied coordinate.
    while True:
        tuple_coords = (random.randint(0, 2), random.randint(0, 2))
        if coords_occupied(grid, tuple_coords):
            continue
        print(f'Computer selected coordinates {tuple_coords}')
        return tuple_coords


def computer_move(grid):
    # Has the computer 'take a turn' by setting the value to 'O', having it select coordinates,
    # marking the grid and then printing it to the terminal.
    value = 'O'
    coords = computer_coords(grid)
    mark_grid(grid, coords, value)
    print_grid(grid)


def player_move(grid):
    # Has the player take a turn. Gets coordinates from them, then checks if they are occupied.
    # Once unoccupied coordinates are found, marks the grid on the coordinates and prints them.
    value = 'X'
    while True:
        coords = get_coords()
        if coords_occupied(grid, coords):
            print("Coordinates occupied. Please select other coordinates.")
            continue
        break
    mark_grid(grid, coords, value)
    print_grid(grid)


def winner_declared(grid, comp_turn):
    # Checks if the player whose turn it is has won or not. If they did win, returns their value.
    if comp_turn:
        value = 'O'
    else:
        value = 'X'
    if someone_won(grid, value):
        return value
    return False


def game():
    # This function executes one game.
    grid = make_grid()
    turn_order = input("Do you want to go first? (y/n): ")
    comp_turn = None
    turns = 0
    # If the player has selected to go second, this code executes and the computer takes
    # the first turn. Then we set the comp_turn variable to False.
    if turn_order == 'n':
        computer_move(grid)
        comp_turn = False
        turns += 1
    # This is the main game loop. The loop checks whose turn it is and then has that player take their turn.
    while True:
        if comp_turn is None:
            comp_turn = False
        if not comp_turn:
            player_move(grid)
        elif comp_turn:
            computer_move(grid)
        # Here we check if the player whose turn it is has won yet.
        if winner_declared(grid, comp_turn):
            value = winner_declared(grid, comp_turn)
            if value == 'X':
                print("You win!")
            else:
                print("You lose!")
            break
        # If no one has won yet, the turn is changed to the other turn and the turn number goes up.
        comp_turn = not comp_turn
        turns += 1
        # If nine turns have been taken and no one has won, the game is by definition a draw (since the board
        # will be full).
        if turns == 9:
            print("it's a tie!")
            break

# This is the main loop executed on startup. An intro is given and the first game is run. Then the player
# can choose to play again or quit.
def main():
    print("Welcome to tic-tac-toe! You will be player X.")
    game()
    while True:
        response = input('Do you want to play again? (y/n): ')
        if response == 'n':
            print('Thanks for playing!')
            break
        elif response == 'y':
            game()
        else:
            print("Please input \'y\' or \'n\'.")


main()
