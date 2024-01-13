import re


# region Functions
def allowed_chars(string):
    if len(string) == 9:
        character_regex = re.compile(r'[^_XO.]')
        string = character_regex.search(string)
        return not bool(string)
    else:
        return False


def convert_to_grid(board):
    grid_layout = [list(board[0:3]), list(board[3:6]), list(board[6:])]
    return grid_layout


def draw_current_game(board):
    horizontal_border = "---------"
    vertical_border = "|"
    print(horizontal_border)
    print(vertical_border + " " + board[0][0] + " " + board[0][1] + " " + board[0][2] + " " + vertical_border)
    print(vertical_border + " " + board[1][0] + " " + board[1][1] + " " + board[1][2] + " " + vertical_border)
    print(vertical_border + " " + board[2][0] + " " + board[2][1] + " " + board[2][2] + " " + vertical_border)
    print(horizontal_border)


def verify_game_state(game_board):
    current_board_layout = game_board

    def too_many_turns(board):
        diff_x_o = 0  # Difference between X and O moves should be 1 or 0
        current_board = board
        for i in range(3):
            for j in range(3):
                if current_board[i][j] == 'X':
                    diff_x_o += 1
                elif current_board[i][j] == 'O':
                    diff_x_o -= 1
        if abs(diff_x_o) > 1:
            return "Impossible"
        else:
            return "Valid"

    def winning_condition(board):
        x_winner = False
        o_winner = False
        draw_game = False
        unfinished = False

        board_string = ""
        for i in range(3):
            for j in range(3):
                board_string += board[i][j]

        winning_patterns = ("???......",
                            "...???...",
                            "......???",
                            "?..?..?..",
                            ".?..?..?.",
                            "..?..?..?",
                            "?...?...?",
                            "..?.?.?..")

        marks = ("X", "O")
        for pattern in winning_patterns:
            for mark in marks:
                if re.match(pattern.replace("?", mark), board_string):
                    if mark == "X":
                        x_winner = True
                    if mark == "O":
                        o_winner = True

        if not x_winner and not o_winner:
            if "_" in board_string or " " in board_string:
                unfinished = True
            else:
                draw_game = True

        if x_winner and not o_winner and not draw_game and not unfinished:
            return "X wins"
        elif o_winner and not x_winner and not draw_game and not unfinished:
            return "O wins"
        elif draw_game and not x_winner and not o_winner and not unfinished:
            return "Draw"
        elif unfinished and not x_winner and not o_winner and not draw_game:
            return "Game not finished"
        else:
            return "Impossible"

    status = "Valid"
    while status == "Valid":
        if (too_many_turns(current_board_layout)) != "Valid":  # Check for too many turns taken by a side
            status = "Impossible"
            break

        winner = winning_condition(current_board_layout)  # Check for winner
        if winner != "Valid":
            status = winner
            break

    return status


def play_a_game(board):
    board_layout = board
    current_player = 1
    next_move_input = input()
    next_move = next_move_input.split()
    move_status = "Invalid"
    while move_status == "Invalid":
        try:
            for i in range(len(next_move)):
                next_move[i] = int(next_move[i])
            for i in range(len(next_move)):
                if next_move[i] < 1 or next_move[i] > 3:
                    raise RuntimeError

            row = next_move[0] - 1
            col = next_move[1] - 1
            if board_layout[row][col] == "X" or board_layout[row][col] == "O":
                print("This cell is occupied! Choose another one!")
                next_move_input = input()
                next_move = next_move_input.split()
                continue
            else:
                if current_player == 1:
                    board_layout[row][col] = "X"
                    game_status = verify_game_state(board_layout)
                    if game_status != "Game not finished":
                        draw_current_game(board_layout)
                        print(game_status)
                    else:
                        draw_current_game(board_layout)
                        current_player = 2
                        next_move_input = input()
                        next_move = next_move_input.split()
                        continue
                elif current_player == 2:
                    board_layout[row][col] = "O"
                    game_status = verify_game_state(board_layout)
                    if game_status != "Game not finished":
                        draw_current_game(board_layout)
                        print(game_status)
                    else:
                        draw_current_game(board_layout)
                        current_player = 1
                        next_move_input = input()
                        next_move = next_move_input.split()
                        continue

            move_status = "Valid"

        except ValueError:
            print("You should enter numbers!")
            next_move_input = input()
            next_move = next_move_input.split()
            continue
        except RuntimeError:
            print("Coordinates should be from 1 to 3!")
            next_move_input = input()
            next_move = next_move_input.split()
            continue


# endregion

# region Main Execution

initial_board_layout = "         "
game_grid = convert_to_grid(initial_board_layout)
draw_current_game(game_grid)
play_a_game(game_grid)

###################################################################################################
# This is an old testing section that can be re-enabled later to check an existing game in progress
#
# initial_board_layout = input()
# if not allowed_chars(initial_board_layout):
#     print("Invalid game configuration detected")
# else:
#     game_grid = convert_to_grid(initial_board_layout)
# verify_game_state(game_grid)
###################################################################################################


# endregion
