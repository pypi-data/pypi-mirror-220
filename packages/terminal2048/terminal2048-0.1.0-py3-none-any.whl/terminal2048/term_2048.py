#! /usr/bin/env python
import argparse
from enum import Enum
import random

from blessed import Terminal, keyboard

from typing import List, Tuple, Optional, Dict

Board = List[List[int]]

def css_color_to_rgb(css_color: str) -> Tuple[int, int, int]:
    css_color = css_color.lstrip('#')  # Remove the '#' if present

    # Extract the red, green, and blue components
    red   = int(css_color[0:2], 16)
    green = int(css_color[2:4], 16)
    blue  = int(css_color[4:6], 16)

    return red, green, blue

# These colors are taken from the original 2048 game at https://play2048.co/
CSS_COLORS_2048 = {
    0:    '#cdc1b4',
    2:    '#eee4da',
    4:    '#eee1c9',
    8:    '#f3b27a',
    16:   '#f69664',
    32:   '#f77c5f',
    64:   '#f75f3b',
    128:  '#edd073',
    256:  '#edcc62',
    512:  '#edc950',
    1024: '#edc53f',
    2048: '#edc22e',
    4096: '#00ff00',
    8192: '#ff00ff',
}
BLESSED_COLORS_2048 = {k:css_color_to_rgb(v) for k,v in CSS_COLORS_2048.items()}

class GameAction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    END_GAME = 'endgame'

# Function to initialize the board with two random tiles
def initialize_board(w=4, h=4, highest_start_value=4) -> List[List[int]]:
    board: Board = [[0 for _ in range(w)] for _ in range(h)]
    add_new_tile(board)
    add_new_tile(board)
    if highest_start_value > 4:
        add_new_tile(board, highest_start_value)
    return board

def css_color_to_rgb(css_color: str) -> Tuple[int, int, int]:
    css_color = css_color.lstrip('#')  # Remove the '#' if present

    # Extract the red, green, and blue components
    red   = int(css_color[0:2], 16)
    green = int(css_color[2:4], 16)
    blue  = int(css_color[4:6], 16)

    return red, green, blue

# Function to print the board
def print_board(board: Board, tile_size:Tuple[int, int], term:Terminal) -> None:
    # cell_w should be at least 5.
    # cell_h should be odd, so that we can center the number in the middle row.
    # (5, 1) is the smallest size that works.
    # (7, 3) is roughly square on my terminal.
    # (12, 5) are large squares. Need a tall terminal otherwise it wraps.
    cell_w, cell_h = tile_size
    head_foot_rows = (cell_h - 1)//2
    blank_cell = ' ' * cell_w

    for row in board:
        cell_strs = []
        blank_strs = []
        for cell in row:
            bg_color = term.on_color_rgb(*BLESSED_COLORS_2048[cell])
            num_str = str(cell).center(cell_w) if cell != 0 else blank_cell
            blank_strs.append(bg_color + blank_cell) 
            cell_strs.append(bg_color + term.black_bold + num_str)
        blank_row = ''.join(blank_strs)
        cell_row = ''.join(cell_strs)

        header = '\n'.join([blank_row for _ in range(head_foot_rows)])
        opt_newline = '\n' if header else ''
        print(f'{header}{opt_newline}{cell_row}{opt_newline}{header}' + term.normal)

    print("\nUse arrow keys (up, down, left, right) to play, 'q' to quit.")

# Function to add a new tile (2 or 4) to the board at a random empty location
def add_new_tile(board: Board, top_value:int|None=None):
    # TODO: this alters board in place. I'd prefer the zero-side-effects version
    # where we create a new board.
    # Big game boards need more than one tile added at a time. Add one tile for
    # every 16 tiles on the board, roughly
    board_w, board_h = len(board[0]), len(board)
    num_to_add = max(1, len(board) * len(board[0]) // 16)
    for i in range(num_to_add):
        empty_tiles: List[Tuple[int, int]] = [(i, j) for i in range(board_h) for j in range(board_w) if board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            new_val = 2 if random.random() < 0.9 else 4
            if top_value is not None:
                new_val = top_value 

            board[i][j] = 2 if random.random() < 0.9 else 4

# Function to merge tiles towards the beginning of the list. 
# We sample from the board differently to do the different move directions
def merge_tiles(row: List[int]) -> Tuple[List[int], int]:
    score = 0
    sparse = [r for r in row if r != 0]
    merged_row: List[int] = []
    i = 0
    while i < len(sparse):
        if i < len(sparse) - 1 and sparse[i] == sparse[i + 1]:
            merged_row.append(sparse[i] * 2)
            score += sparse[i] * 2
            i += 1
        else:
            merged_row.append(sparse[i])
        i += 1
    # fill in the rest with zeros
    while len(merged_row) < len(row):
        merged_row.append(0)
    return merged_row, score    

# Function to move the tiles in the specified direction
def move(board: Board, direction: GameAction) -> Tuple[Board, int]:
    shuffled: List[List[int]] 
    match direction:
        case GameAction.UP:
            shuffled = [list(column) for column in zip(*board)]
        case GameAction.DOWN:
            shuffled = [list(column[::-1]) for column in zip(*board)]
        case GameAction.LEFT:
            shuffled = [list(row) for row in board]
        case GameAction.RIGHT:
            shuffled = [list(row[::-1]) for row in board]

    new_rows_and_scores = list([merge_tiles(row) for row in shuffled]) 
    new_board, scores = zip(*new_rows_and_scores)
    score = sum(scores)

    # re-order correctly
    match direction:
        case GameAction.DOWN:
            new_board = [list(row) for row in zip(*new_board)][::-1]
        case GameAction.UP:
            new_board = [list(row) for row in zip(*new_board)] 
        case GameAction.LEFT:
            new_board = new_board
        case GameAction.RIGHT:
            new_board = [row[::-1] for row in new_board]       

    return list(new_board), score

# Function to check if the game is over (no possible moves left)
def is_game_over(board: Board) -> bool:
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i > 0 and board[i][j] == board[i - 1][j]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j > 0 and board[i][j] == board[i][j - 1]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

def get_arrow(inp: keyboard.Keystroke) -> Optional[GameAction]:
    actions = {
        'KEY_UP': GameAction.UP, 
        'KEY_DOWN': GameAction.DOWN, 
        'KEY_LEFT': GameAction.LEFT, 
        'KEY_RIGHT': GameAction.RIGHT, 
        'q': GameAction.END_GAME, 
        'Q': GameAction.END_GAME, 
    }
    return actions.get(inp.name or str(inp), None)

def greatest_power_of_two(n:int) -> int:
    power = 1
    while power * 2 <= n:
        power *= 2
    return power

def parse_args():
    desc = "2048 game in the terminal. Inspired by https://play2048.co/"
    parser = argparse.ArgumentParser(description=desc)
    
    # Optional arguments
    parser.add_argument("-w", "--width", type=int, default=4, 
        help="Width of the board (default: 4)")
    parser.add_argument("--height", type=int, default=4, 
        help="Height of the board (default: 4)")
    parser.add_argument("-s", "--size", choices=['S', 'M', 'L', 'XL'], default='M', 
        help="Board size (options: S, M, L, XL; default: M)")
    parser.add_argument("--start_value", type=greatest_power_of_two, default=4, 
        help="Highest starting tile value (default: 4)")

    args = parser.parse_args()
    return args

# Main game loop
def main() -> None:
    args = parse_args()

    board: Board = initialize_board(args.width, args.height, args.start_value)

    board_size: Tuple[int, int]
    tile_sizes = {
        'S': (5, 1),
        'M': (7, 3),
        'L': (12, 5),
        'XL': (16, 7),
    }
    tile_size = tile_sizes.get(args.size, tile_sizes['M'])

    inp = None
    term = Terminal()
    print(term.home + term.clear)

    score = 0

    with term.hidden_cursor(), term.cbreak(), term.location():
        while True:
            print(term.home + '2048 - Text Version')
            print(f'Score: {score}')
            print_board(board, tile_size, term)
            if is_game_over(board):
                print(f'Game Over! Your score was {score}.')
                print('Hit a key to continue...')
                inp = term.inkey(timeout=None)                
                break

            # direction: str = input().lower()
            inp = term.inkey(timeout=None)
            action = get_arrow(inp)
            if action == GameAction.END_GAME:
                print("Quitting the game...")
                break

            if action:
                new_board, new_score = move(board, action)
                if new_board != board:
                    board = new_board
                    score += new_score
                    add_new_tile(board)

if __name__ == "__main__":
    main()
