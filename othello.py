import sys
from typing import List, Tuple, Optional

BOARD_SIZE = 8

# Directions for scanning: N, NE, E, SE, S, SW, W, NW
DIRECTIONS = [
    (-1, 0), (-1, 1), (0, 1), (1, 1),
    (1, 0), (1, -1), (0, -1), (-1, -1)
]

EMPTY = '.'
BLACK = 'B'
WHITE = 'W'


def create_board() -> List[List[str]]:
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board


def print_board(board: List[List[str]]) -> None:
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for idx, row in enumerate(board):
        print(str(idx) + " " + " ".join(row))
    print()


def on_board(x: int, y: int) -> bool:
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def valid_moves(board: List[List[str]], player: str) -> List[Tuple[int, int]]:
    opponent = WHITE if player == BLACK else BLACK
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] != EMPTY:
                continue
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                has_opponent_between = False
                while on_board(nx, ny) and board[nx][ny] == opponent:
                    nx += dx
                    ny += dy
                    has_opponent_between = True
                if has_opponent_between and on_board(nx, ny) and board[nx][ny] == player:
                    moves.append((x, y))
                    break
    return moves


def make_move(board: List[List[str]], x: int, y: int, player: str) -> bool:
    if board[x][y] != EMPTY:
        return False
    opponent = WHITE if player == BLACK else BLACK
    to_flip = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        path = []
        while on_board(nx, ny) and board[nx][ny] == opponent:
            path.append((nx, ny))
            nx += dx
            ny += dy
        if path and on_board(nx, ny) and board[nx][ny] == player:
            to_flip.extend(path)
    if not to_flip:
        return False
    board[x][y] = player
    for fx, fy in to_flip:
        board[fx][fy] = player
    return True


def score(board: List[List[str]]) -> Tuple[int, int]:
    black = sum(row.count(BLACK) for row in board)
    white = sum(row.count(WHITE) for row in board)
    return black, white


def game_over(board: List[List[str]]) -> bool:
    return not valid_moves(board, BLACK) and not valid_moves(board, WHITE)


def play_game() -> None:
    board = create_board()
    current_player = BLACK
    while not game_over(board):
        print_board(board)
        moves = valid_moves(board, current_player)
        if not moves:
            print(f"{current_player} has no valid moves. Skipping turn.")
            current_player = WHITE if current_player == BLACK else BLACK
            continue
        print(f"Current player: {current_player}")
        print("Valid moves:", moves)
        try:
            move_input = input("Enter move as 'row col': ")
            if move_input.lower() in ('quit', 'exit'):
                print("Game aborted.")
                return
            x_str, y_str = move_input.split()
            x, y = int(x_str), int(y_str)
        except ValueError:
            print("Invalid input. Try again.")
            continue
        if (x, y) not in moves:
            print("Invalid move. Try again.")
            continue
        make_move(board, x, y, current_player)
        current_player = WHITE if current_player == BLACK else BLACK
    black_score, white_score = score(board)
    print_board(board)
    print(f"Game over! Black: {black_score}, White: {white_score}")
    if black_score > white_score:
        print("Black wins!")
    elif white_score > black_score:
        print("White wins!")
    else:
        print("It's a tie!")


if __name__ == '__main__':
    play_game()
