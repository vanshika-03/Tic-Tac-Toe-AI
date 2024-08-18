
from flask import Flask, request, jsonify  # Import Flask modules
from flask_cors import CORS  # Import CORS module to handle cross-origin requests
import copy  # Import copy module to make deep copies of the board
import math  # Import math module for infinity

X = 'X'  # Constant for player X
O = 'O'  # Constant for player O

app = Flask(__name__)  # Create a Flask app instance
CORS(app)  # Enable CORS for the app

# Determine which player's turn it is
def player(board):
    countX = 0
    countO = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX += 1
            if board[row][col] == O:
                countO += 1
    return O if countX > countO else X

# Get all possible actions (empty cells)
def actions(board):
    possibleAction = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == None:
                possibleAction.add((row, col))
    return possibleAction

# Apply an action to the board and return the new board state
def result(board, action):
    if action not in actions(board):
        raise Exception("Not valid action")
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy

# Check if a player has won by completing a row
def checkRow(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False

# Check if a player has won by completing a column
def checkCol(board, player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False

# Check if a player has won by completing the left diagonal
def diagonalL(board, player):
    return all(board[i][i] == player for i in range(len(board)))

# Check if a player has won by completing the right diagonal
def diagonalR(board, player):
    return all(board[i][len(board) - i - 1] == player for i in range(len(board)))

# Determine the winner of the game
def winner(board):
    if checkRow(board, X) or checkCol(board, X) or diagonalR(board, X) or diagonalL(board, X):
        return X
    elif checkRow(board, O) or checkCol(board, O) or diagonalR(board, O) or diagonalL(board, O):
        return O
    else:
        return None

# Check if the game has ended
def terminal(board):
    return winner(board) is not None or all(cell is not None for row in board for cell in row)

# Get the utility value of the board (1 for X win, -1 for O win, 0 for draw)
def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Minimax helper function for maximizing player
def maximising(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minimising(result(board, action)))
    return v

# Minimax helper function for minimizing player
def minimising(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maximising(result(board, action)))
    return v

# Minimax algorithm to determine the best move
def minimax(board):
    if terminal(board):
        return None
    if player(board) == X:
        plays = [[minimising(result(board, action)), action] for action in actions(board)]
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    else:
        plays = [[maximising(result(board, action)), action] for action in actions(board)]
        return sorted(plays, key=lambda x: x[0])[0][1]

# Flask route to handle move requests
@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    move = minimax(board)
    return jsonify({'row': move[0], 'col': move[1]})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
