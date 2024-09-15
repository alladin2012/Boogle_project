from Board import Board
from Cell import Cell
from GameTimer import GameTimer
import tkinter as tk
from typing import Literal, Optional, Tuple, List, Dict, Set
from boggle_board_randomizer import randomize_board
from ex11_utils import is_valid_path, max_score_paths
from random import randint

Path = List[Tuple[int, int]]

class Difficulty:
    EASY = "easy"
    MEDIUM = "mid"
    HARD = "hard"

class Game:
    """Game - Boggle Game.
        The game is initialized with a board size, the time for its timer,
        words dictionary set and an optional difficulty (of type {Difficulty}).
        Creates the GUI representation and flow of the Boggle game."""

    BACKGROUND_COLOR = "lightblue"
    BOARD_COLOR = "lightgrey"
    SELECTED_CELL_COLOR = "cyan"

    def __init__(self, board_size: int, countdown: Tuple[int, int], words: Set[str],
                 difficulty: Literal["easy", "mid", "hard"]=Difficulty.EASY):
        #general
        self.board: Board = Board(board_size)
        self.window = tk.Tk()
        self.frame = tk.Frame(self.window, bg=self.BACKGROUND_COLOR)
        self.canvas: tk.Canvas
        self._init_window()
        self._init_background()
        self.all_words: Set[str] = words
        self.running = False
        self.words_bank: Dict[str, Path] = {}
        self.curr_path: Path = []
        self.curr_word: str = ""
        self.curr_score = 0
        self.best_score = 0
        self.solutions: List[Path] = []
        self.difficulty = difficulty
        #timer
        minutes, seconds = countdown
        self.timer = GameTimer(minutes, seconds, self.BACKGROUND_COLOR)
        self.timer_id: Optional[str]
        #buttons
        self._declare_buttons()
        self._add_timer()
        self._add_start_button()

    def start(self):
        """Main game command - starting the game."""
        self.window.mainloop()

    #general GUI functions
    def _init_window(self):
        self.window.title("Boggle")

    def _init_background(self):
        """Initialize all the major background GUI elements of the game."""
        self.frame.pack(fill=tk.BOTH, expand=True)
        #general canvas (will be filled later)
        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg=self.BOARD_COLOR)
        self.canvas.grid(row=0, column=0, columnspan=1, padx=20, pady=20)
        #words section - canvas, current word, section label and finished words
        words_section_canvas = tk.Canvas(self.frame, width=200, height=100, bg="white")
        words_section_canvas.grid(row=0, column=2, columnspan=4, padx=10, pady=0)
        self.curr_word_text = tk.Label(self.frame, font=("Arial", 16), background="white")
        self.curr_word_text.pack(in_=words_section_canvas, side=tk.TOP, fill=tk.BOTH)
        words_section_label = tk.Label(self.frame, font=("Arial", 16), text="Words Found", background="white")
        words_section_label.pack(in_=words_section_canvas, side=tk.TOP, fill=tk.BOTH)
        #scrollbar for words section, and words list
        words_section_sbar = tk.Scrollbar(self.frame)
        words_section_sbar.pack(in_=words_section_canvas, side=tk.RIGHT, fill=tk.Y)
        self.words_section_list = tk.Listbox(self.frame, yscrollcommand=words_section_sbar.set,
                                        font=("Arial", 14), background="white")
        self.words_section_list.pack(in_=words_section_canvas, side=tk.LEFT, fill=tk.BOTH)
        words_section_sbar.config(command=self.words_section_list.yview)
        #score section - canvas, labels, current score and best score
        score_c = tk.Canvas(self.frame, width=200, height=150)
        score_c.grid(row=1, column=2, columnspan=4, padx=10, pady=0)
        score_l = tk.Label(self.frame, font=("Arial", 16), text="Score")
        score_l.place(in_=score_c, rely=.2, relx=.5, anchor= tk.CENTER)
        self.curr_score_t = tk.Label(self.frame, font=("Arial", 14))
        self.curr_score_t.place(in_=score_c, x=0, y=50)
        best_score_l = tk.Label(self.frame, font=("Arial", 16), text="High Score")
        best_score_l.place(in_=score_c, rely=.6, relx=.5, anchor= tk.CENTER)
        self.best_score_t = tk.Label(self.frame, font=("Arial", 14))
        self.best_score_t.place(in_=score_c, x=0, y=120)


    #buttons GUI functions 
    def _declare_buttons(self):
        self.start_game_button: tk.Button = tk.Button()
        self.reset_game_button: tk.Button = tk.Button()
        self.finish_game_button: tk.Button = tk.Button()
        self.reset_word_button: tk.Button = tk.Button()
        self.check_word_button: tk.Button = tk.Button()
        self.hint_button: tk.Button = tk.Button()

    def _add_start_button(self):
        """Add the Start Game button to the GUI."""
        #remove all in-game buttons first
        self.finish_game_button.destroy()
        self.reset_word_button.destroy()
        self.check_word_button.destroy()
        self.hint_button.destroy()
        self.start_game_button = tk.Button(self.frame, text="Start Game", command=self._start_game)
        self.start_game_button.grid(row=4, column=0, columnspan=1, padx=20, pady=10)

    def _add_check_word_button(self):
        """Add the Check Word button to the GUI."""
        self.check_word_button = tk.Button(self.frame, text="Check Word", command=self._check_word)
        self.check_word_button.grid(row=3, column=2, columnspan=1, padx=20, pady=20)

    def _add_reset_word_button(self):
        """Add the Reset Word button to the GUI."""
        self.reset_word_button = tk.Button(self.frame, text="Reset Word", command=self._reset_word)
        self.reset_word_button.grid(row=3, column=3, columnspan=1, padx=20, pady=10)

    def _add_hint_button(self):
        """Add the Get Hint button to the GUI."""
        self.hint_button = tk.Button(self.frame, text="Get Hint", command=self._get_hint)
        self.hint_button.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

    def _add_finish_button(self):
        """Add the Finish Game button to the GUI."""
        self.start_game_button.destroy()
        self.finish_game_button = tk.Button(self.frame, text="Finish Game", command=self._finish_game)
        self.finish_game_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)


    #buttons functionality functions
    def _start_game(self):
        """Starts the game - start the timer, add the in-game buttons and create the board."""
        #start game and timer
        self.running = True
        self.timer.start()
        self.timer_id = self._start_timer()
        #add in-game buttons
        self._add_finish_button()
        self._add_reset_word_button()
        self._add_check_word_button()
        if (self.difficulty != Difficulty.HARD):
            self._add_hint_button()
        #reset previous session
        self._reset_game_progress()
        #add board
        self._create_board(self.board, randomize_board(), self.frame, self.BOARD_COLOR)
        self.gui_board = self.board.gui(100, 100)

    def _check_word(self):
        """Check the current submitted word against the words dictionary.
            Update the score accordingly."""
        opt_word = is_valid_path(self.board.get_str_board(), self.curr_path, self.all_words)
        if (opt_word is not None):
            if (self.curr_word not in self.words_bank.keys()):
                self.words_bank[opt_word] = self.curr_path
                self.curr_score += self._get_score_from_path(self.curr_path)
                self._update_score_display()
                self._update_found_words_display(opt_word)
                if (self.curr_path in self.solutions):
                    self.solutions.remove(self.curr_path)
        self._reset_word()
        self._update_hint_display(tk.NORMAL)

    def _reset_word(self):
        """"Reset current path."""
        for location in self.curr_path:
            self._update_curr_cell_display_deselected(location)
        self.curr_path = []
        self.curr_word = ""
        self._update_curr_word_display()

    def _get_hint(self):
        """Add cells to the current path for an optional max-score word on the board.
            Number of cells added - according to the difficutly."""
        hint_cells = self._get_optional_hint_cells(self.difficulty)
        if (hint_cells is not None):
            for cell in hint_cells:
                x, y = cell
                self._add_cell_to_path(x, y)

    def _finish_game(self):
        """Finish the current run - set the high score, stop the timer, disable the board
            and change buttons the out-game view."""
        self.best_score = self.curr_score if self.curr_score > self.best_score else self.best_score
        self._update_best_score_display()
        self.timer.stop()
        self.running = False
        self._disable_board()
        self._add_start_button()
        if (self.timer_id is not None):
            self.window.after_cancel(self.timer_id)


    #game flow functions
    def _create_board(self, board: Board, cells: List[List[str]], frame: tk.Frame, cell_bg: str):
        """Create the board with a given letters list and background color."""
        for i in range(len(cells)):
            for j in range (len(cells[0])):
                new_cell = Cell(cells[i][j], frame,
                                command=lambda r=i, c=j: self._add_cell_to_path(r, c),
                                bg=cell_bg)
                board.insert_cell(new_cell, (i, j))
    
    def _reset_game_progress(self):
        """"Reset the game progress - reset all in-game data."""
        self.curr_path = []
        self.words_bank = {}
        self._reset_found_words_display()
        self.curr_word = ""
        self._update_curr_word_display()
        self.curr_score = 0
        self._update_score_display()
        self._enable_board()

    def _start_timer(self):
        """Loop for updating the timer while the game & timer are running."""
        if (self.running and self.timer.get_timer_state()):
            self.timer.update_time()
            return self.window.after(1000, self._start_timer)
        elif (self.running):
            self._finish_game()
    
    def _add_timer(self):
        self.timer.gui(self.frame, (1, 0, 2))

    def _disable_board(self):
        """Disable the board GUI representation."""
        str_board = self.board.get_str_board()
        for i in range(len(str_board)):
            for j in range (len(str_board[0])):
                self._disable_cell_display((i, j))

    def _enable_board(self):
        """Enable the board GUI representation."""
        str_board = self.board.get_str_board()
        for i in range(len(str_board)):
            for j in range (len(str_board[0])):
                self._enable_cell_display((i, j))


    #GUI update functions
    def _update_curr_word_display(self):
        self.curr_word_text.config(text=self.curr_word)

    def _update_curr_cell_display_selected(self, location: Tuple[int, int]):
        cell = self.board.get_cell(location)
        if (cell is not None):
            x, y = location
            self.gui_board[x][y].config(bg=self.SELECTED_CELL_COLOR)
            
    def _update_curr_cell_display_deselected(self, location: Tuple[int, int]):
        cell = self.board.get_cell(location)
        if (cell is not None):
            x, y = location
            self.gui_board[x][y].config(bg=self.BOARD_COLOR)
        
    def _update_found_words_display(self, new_word: str):
        self.words_section_list.insert(0, new_word)

    def _reset_found_words_display(self):
        self.words_section_list.delete(0, tk.END)

    def _update_score_display(self):
        self.curr_score_t.config(text=self.curr_score)
        
    def _update_best_score_display(self):
        self.best_score_t.config(text=self.best_score)

    def _update_hint_display(self, mode: Literal['normal', 'active', 'disabled']):
        self.hint_button.config(state=mode)

    def _disable_cell_display(self, location: Tuple[int, int]):
        cell = self.board.get_cell(location)
        if (cell is not None):
            x, y = location
            self.gui_board[x][y].config(bg=self.BOARD_COLOR, state=tk.DISABLED)
            
    def _enable_cell_display(self, location: Tuple[int, int]):
        cell = self.board.get_cell(location)
        if (cell is not None):
            x, y = location
            self.gui_board[x][y].config(state=tk.NORMAL)


    #util functions    
    def _add_cell_to_path(self, row, col):
        """If the given location is valid, add the cell to the current running path.
            Update the GUI accordingly."""
        if (self._check_location_valid((row, col))):
            letter = self.board.get_cell((row, col))
            assert letter is not None
            self.curr_path.append((row, col))
            cell = self.board.get_cell((row, col))
            self.curr_word += cell.get_content() if cell is not None else ""
            self._update_curr_cell_display_selected((row, col))
            self._update_curr_word_display()
            self._update_hint_display(tk.DISABLED)

    def _check_location_valid(self, location: Tuple[int, int]):
        """Valid location = starting new path OR not in current path + valid move."""
        if (len(self.curr_path) == 0):
            return True
        if (location in self.curr_path):
            return False
        return self.board.is_move_valid(location, self.curr_path[-1])

    def _get_score_from_path(self, path: Path):
        """Score is calculated by path length squared."""
        return len(path) ** 2

    def _get_optional_hint_cells(self, difficulty: str) -> List[Tuple[int, int]]:
        """According to given difficulty, return list of hint cells of
            a max-score word on the board."""
        if (len(self.solutions) == 0):
            self.solutions = max_score_paths(self.board.get_str_board(), set(self.all_words))
        rand_i = randint(0, len(self.solutions) - 1)
        hint_path = self.solutions[rand_i]
        cutoff = 0
        if (difficulty == Difficulty.EASY):
            cutoff = len(hint_path) // 2
        if (difficulty == Difficulty.MEDIUM):
            cutoff = len(hint_path) // 3 or 1
        return hint_path[0:cutoff]
    
    #for debugging purposes
    def _word_from_path(self, path: Path) -> str:
        word = ""
        for location in path:
            cell = self.board.get_cell(location)
            if cell is not None:
                word += cell.get_content()
        return word