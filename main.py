import chess
import chess.engine

# Start the Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci("/Users/luisgustavoolimpio/Documents/GitHub/Stockfish/src/stockfish")

# Create a chess board
board = chess.Board()

def print_board():
    print("   a b c d e f g h")
    print(" +----------------")
    for rank in range(7, -1, -1):
        row = " |"
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece is None:
                row += " ."
            else:
                row += " " + piece.symbol().upper()
        row += f" {rank + 1}"
        print(row)
    print(" +----------------")
    print(f"   {'W' if board.turn == chess.WHITE else 'B'}")
    print("   a b c d e f g h")

def choose_side():
    side = input("Choose your side (w for white, b for black): ")
    if side.lower() == 'w':
        return True
    elif side.lower() == 'b':
        return False
    else:
        print("Invalid choice. Defaulting to white.")
        return True

# Choose the side
player_is_white = choose_side()

# If the player is black, let the engine play the first move
if not player_is_white:
    time_limit = 5
    info = engine.play(board, chess.engine.Limit(time=time_limit))
    pc_move = info.move
    board.push(pc_move)
    print("PC move:", pc_move)

while not board.is_game_over():
    # Print the current state of the board
    print_board()

    # Get user's move
    if (board.turn == chess.WHITE and player_is_white) or (board.turn == chess.BLACK and not player_is_white):
        user_move = input("Enter your move (in UCI format, e.g. e2e4): ")
        try:
            # Try to execute the move
            move = chess.Move.from_uci(user_move)
            if board.is_legal(move):
                board.push(move)
            else:
                print("Invalid move")
                continue
        except:
            print("Invalid move")
            continue
    else:
        # Use the Stockfish engine to suggest a move
        time_limit = 5
        info = engine.play(board, chess.engine.Limit(time=time_limit))
        pc_move = info.move
        board.push(pc_move)
        print("PC move:", pc_move)

# Print the result of the game
result = board.result()
if result == "1-0":
    print("You won!" if player_is_white else "You lost!")
elif result == "0-1":
    print("You lost!" if player_is_white else "You won!")
else:
    print("It's a draw!")

# Quit the engine
engine.quit()
