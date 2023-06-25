import tkinter as tk

# The game board
board = ['-'] * 9

# Constants for players and empty cells
AI = 'X'
PLAYER = 'O'
EMPTY = '-'

# Possible winning combinations
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]               # Diagonals
]

# Create the Tkinter window
window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry("500x500")
window.configure(bg="#333333")

# Create a label to display messages
message_label = tk.Label(window, text="Welcome to Tic Tac Toe!", fg="#FFFFFF", bg="#333333", font=("Arial", 14))
message_label.pack(pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(window, bg="#333333")
button_frame.pack()

# Create the buttons for the game board
buttons = []
for i in range(9):
    button = tk.Button(button_frame, text="", width=8, height=3, font=("Arial", 20), bg="#555555", fg="#FFFFFF", bd=0)
    buttons.append(button)
    button.grid(row=i // 3, column=i % 3, padx=10, pady=10)

def update_board():
    """Updates the text on the buttons based on the current state of the board."""
    for i in range(9):
        buttons[i].config(text=board[i])

def button_click(index):
    """Handles the button click event."""
    if board[index] != EMPTY:
        return

    make_move(board, index, PLAYER)
    update_board()

    if is_winner(board, PLAYER):
        message_label.config(text="Congratulations! You won!")
        disable_buttons()
        return
    elif is_board_full(board):
        message_label.config(text="It's a draw!")
        disable_buttons()
        return

    ai_move = get_best_move(board)
    make_move(board, ai_move, AI)
    update_board()

    if is_winner(board, AI):
        message_label.config(text="Sorry, you lost!")
        disable_buttons()
        return
    elif is_board_full(board):
        message_label.config(text="It's a draw!")
        disable_buttons()
        return

def disable_buttons():
    """Disables all the buttons."""
    for button in buttons:
        button.config(state=tk.DISABLED)

def enable_buttons():
    """Enables all the buttons."""
    for button in buttons:
        button.config(state=tk.NORMAL)

def print_board(board):
    """Prints the current state of the board."""
    for i in range(0, 9, 3):
        print(board[i] + ' | ' + board[i + 1] + ' | ' + board[i + 2])
    print()

def get_empty_cells(board):
    """Returns a list of indices of empty cells on the board."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]

def is_winner(board, player):
    """Checks if the specified player has won the game."""
    for combination in WINNING_COMBINATIONS:
        if all(board[i] == player for i in combination):
            return True
    return False

def is_board_full(board):
    """Checks if the board is full."""
    return EMPTY not in board

def make_move(board, index, player):
    """Makes a move on the board at the specified index for the specified player."""
    board[index] = player

def minimax(board, depth, is_maximizing):
    """The Minimax algorithm for determining the best move for the AI player."""
    if is_winner(board, AI):
        return 1
    elif is_winner(board, PLAYER):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for index in get_empty_cells(board):
            make_move(board, index, AI)
            score = minimax(board, depth + 1, False)
            make_move(board, index, EMPTY)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for index in get_empty_cells(board):
            make_move(board, index, PLAYER)
            score = minimax(board, depth + 1, True)
            make_move(board, index, EMPTY)
            best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    """Returns the index of the best move for the AI player using the Minimax algorithm."""
    best_score = float('-inf')
    best_move = None
    for index in get_empty_cells(board):
        make_move(board, index, AI)
        score = minimax(board, 0, False)
        make_move(board, index, EMPTY)
        if score > best_score:
            best_score = score
            best_move = index
    return best_move

def play_game():
    """Plays a game of tic-tac-toe."""
    update_board()
    enable_buttons()
    message_label.config(text="Welcome to Tic Tac Toe!")

# Add button click event handlers
for i in range(9):
    buttons[i].config(command=lambda index=i: button_click(index))

# Start the game
play_game()

# Start the Tkinter event loop
window.mainloop()