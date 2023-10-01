from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 's3cr3t'

@app.route('/')
def index():
    if 'board' not in session or 'user_wins' not in session or 'ai_wins' not in session or 'message' not in session:
        session['board'] = [""] * 9
        session['user_wins'] = 0
        session['ai_wins'] = 0
        session['message'] = ""
    winner = check_winner(session['board'], "O") or check_winner(session['board'], "X")
    return render_template('tictactoe.html', board=session['board'], message=session['message'],
                           user_wins=session['user_wins'], ai_wins=session['ai_wins'], winner=winner)
@app.route('/move', methods=['POST'])
def move():
    position = int(request.form.get('position'))
    if session['board'][position] == "":
        session['board'][position] = "O"
        winner = check_winner(session['board'], "O")
        if winner == "O":
            session['user_wins'] += 1
            session['message'] = "User wins!"
        else:
            ai_move(session['board'])
            winner = check_winner(session['board'], "X")
            if winner == "X":
                session['ai_wins'] += 1
                session['message'] = "AI assistant wins!"
            elif winner == "tie":
                session['message'] = "It's a tie!"
            else:
                session['message'] = ""
        session.modified = True
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session['board'] = [""] * 9  # Reset the board
    session['message'] = ""  # Reset the message
    session.modified = True
    return redirect(url_for('index'))

def ai_move(board):
    best_score = -float('inf')
    best_move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    if best_move != -1:
        board[best_move] = "X"

def minimax(board, depth, is_maximizing):
    winner = check_winner(board, "O") or check_winner(board, "X")
    scores = {"X": 1, "O": -1, "tie": 0}
    if winner is not None:
        return scores[winner]

    if is_maximizing:
        best_score = -float('inf')
        symbol = "X"
    else:
        best_score = float('inf')
        symbol = "O"

    for i in range(9):
        if board[i] == "":
            board[i] = symbol
            score = minimax(board, depth + 1, not is_maximizing)
            board[i] = ""
            best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    return best_score

def check_winner(board, player):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combination in win_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] == player:
            return player  # Return the player (either "O" or "X") if a win is found
    if "" not in board:  # The board is full
        return "tie"  # Return "tie" if the board is full and no winner is found
    return None  # Return None if the game is still ongoing

if __name__ == "__main__":
    app.run(debug=True)
