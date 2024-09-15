import tkinter as tk
from typing import List, Optional, Tuple
from Cell import Cell

class Board:
    """Board - Represents a board of cells.
        The board has a GUI representation of a list of {Cell}s.
        The board is initiated with empty cells (None) for a given size,
        and later on can be populated with new {Cell}s."""
    OPTIONAL_MOVES = [(-1, -1), (-1, 0), (1, 0), (0, -1), (0, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]

    def __init__(self, board_size: int):
        self.board: List[List[Optional[Cell]]] = self._init_board(board_size)

    def _init_board(self, board_size: int) -> List[List[Optional[Cell]]]:
        """Initiate an empty board of given size."""
        return [[None for _ in range(board_size)] for _ in range(board_size)]

    def get_cell(self, cell_loc: Tuple[int, int]) -> Optional[Cell]:
        """Return the {Cell} in a given location, if that location is valid. None otherwise."""
        if (not self._is_valid_location(cell_loc)):
            return None
        x, y = cell_loc
        return self.board[x][y]

    def get_str_board(self) -> List[List[str]]:
        """Return a board with String representation of its {Cell}s."""
        str_board: List[List[str]] = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[0])):
                cell = self.get_cell((i, j))
                if (cell is not None):
                    row.append(cell.get_content())
            str_board.append(row)
        return str_board
    
    def is_move_valid(self, new_location: Tuple[int, int], current_location: Tuple[int, int]):
        """For a given new location, check if the move is valid from a given current location
            on the board."""
        new_x, new_y = new_location
        curr_x, curr_y = current_location
        for move in self.OPTIONAL_MOVES:
            move_x, move_y = move
            if (curr_x + move_x == new_x and curr_y + move_y == new_y):
                return True
        return False
    
    def _is_valid_location(self, location: Tuple[int, int]) -> bool:
        """Check if the location is on the board's boundaries."""
        x, y = location
        return (0 <= x < len(self.board) and 0 <= y < len(self.board[0]))
    
    def insert_cell(self, new_cell: Cell, location: Tuple[int, int]) -> bool:
        """Insert a new {Cell} to the board. Insertion is done by placing the new cell
            in the given location (needs to be a valid location).
            Returns success or failure."""
        if (not self._is_valid_location(location)):
            print("Not valid: ", location)
            return False
        x, y = location
        self.board[x][y] = new_cell
        return True
    
    def gui(self, cell_height, cell_width) -> List[List[tk.Button]]:
        """Create the GUI representation of the board."""
        gui_board = []
        for row in range(len(self.board)):
            curr_row = []
            for col in range(len(self.board[0])):
                cell = self.board[row][col]
                if (cell is not None):
                    gui_cell = cell.gui()
                    gui_cell.place(x=col * cell_width + 22, y=row * cell_height + 22,
                                   width=cell_width, height=cell_height)
                    curr_row.append(gui_cell)
            gui_board.append(curr_row)
        return gui_board
