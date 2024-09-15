from typing import List, Tuple, Iterable, Optional, Set, Dict

Board = List[List[str]]
Path = List[Tuple[int, int]]

#CONSTS
OPTIONAL_MOVES = [(-1, -1), (-1, 0), (1, 0), (0, -1), (0, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """Check the validity of a given path for a given board and words dictionary.
        Returns the word if its valid, None otherwise."""
    if (isinstance(words, dict)):
        words = words.keys()
    optinal_word =""
    previous_row, previous_col = -1, -1
    for point in path:
        start_row, start_col= point
        if _on_board(board ,start_row, start_col):
            if previous_row + previous_col != -2:
                space_row = previous_row - start_row
                space_col = previous_col - start_col
                if  1 >= space_row >= - 1 and 1 >= space_col >= - 1:
                    optinal_word += board[start_row][start_col]
            else:
                optinal_word += board[start_row][start_col]
        previous_row, previous_col = start_row, start_col
    if optinal_word in words:
        return optinal_word
    else:
        return None

def _on_board(board: Board, row: int, col: int) -> bool:
    """Check if a location is valid on the board"""
    if row < len(board) and row >= 0:
        if col < len(board[0]) and col >= 0:
            return True
    return False


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """Find valid paths of given length on the board using the given words dictionary."""
    if (isinstance(words, dict)):
        words = words.keys()
    words_on_board = set(filter(lambda word: _is_word_on_board(board, word), words))
    paths: List[Path] = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            #start with current cell
            start_path = [(i, j)]
            start_cell = board[i][j]
            start_words = _words_starts_with(words_on_board, board[i][j])
            #add length n paths for current cell
            _find_length_n_paths_helper(n, board, start_words, i, j, start_cell, start_path, paths)
    return paths

def _find_length_n_paths_helper(n: int, board: Board, words: Set[str], i:int, j: int,
                              curr_word: str, curr_path: Path, finished_paths: List[Path]):
    """Iterate the board, find paths of length n that fit a word in the words set.
        During a spefiic path-trial, filter out words that won't fit."""
    if (len(curr_path) == n):
        #finish case: path length is n
        if (curr_word in words):
            finished_paths.append(curr_path.copy())
        return
    if (len(words) == 0):
        return
    
    for move in OPTIONAL_MOVES:
        next_i = i + move[0]
        next_j = j + move[1]
        if (_safe_to_move(next_i, next_j, board, curr_path)):
            #move forward
            new_word = curr_word + board[next_i][next_j]
            new_path = curr_path + [(next_i, next_j)]
            #filter out words that won't fit
            new_words = _words_starts_with(words, new_word)
            _find_length_n_paths_helper(n, board, new_words, next_i, next_j,
                                            new_word, new_path, finished_paths)

def _words_starts_with(words: Set[str], word: str) -> Set[str]:
    """"Return all words from the given Set that starts with the given word."""
    return set([curr_word for curr_word in words if curr_word.startswith(word)])


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """Find valid paths for words of given length on the board using the given words dictionary."""
    if (isinstance(words, dict)):
        words = words.keys()
    n_length_words = set(filter(lambda word: len(word) == n, words))
    n_length_words = set(filter(lambda word: _is_word_on_board(board, word), n_length_words))
    paths: List[Path] = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            #start with current cell
            start_path = [(i, j)]
            start_cell = board[i][j]
            start_words = _words_starts_with(n_length_words, board[i][j])
            #add length n words for current cell
            _find_length_n_word_paths(n, board, start_words, i, j, start_cell, start_path, paths)
    return paths

def _find_length_n_word_paths(n: int, board: Board, words: Set[str], i:int, j: int,
                              curr_word: str, curr_path: Path, finished_paths: List[Path]):
    """Iterate the board, find paths that fit a word of length n in the words set.
        During a spefiic path-trial, filter out words that won't fit."""
    if (len(curr_word) > n):
        #in case last cell inserted was bigger than one letter
        return
    if (len(curr_word) == n):
        #finish case: word length is n
        if (curr_word in words):
            finished_paths.append(curr_path.copy())
        return
    if (len(words) == 0):
        #prune branches that don't have any words left
        return
    
    for move in OPTIONAL_MOVES:
        next_i = i + move[0]
        next_j = j + move[1]
        if (_safe_to_move(next_i, next_j, board, curr_path)):
            #move forward
            new_word = curr_word + board[next_i][next_j]
            new_path = curr_path + [(next_i, next_j)]
            #filter out words that won't fit current path
            new_words = _words_starts_with(words, new_word)
            _find_length_n_word_paths(n, board, new_words, next_i, next_j,
                                            new_word, new_path, finished_paths)
            
def _safe_to_move(next_i: int, next_j: int, board: Board, path: Path) -> bool:
    """"Check if the given next location is valid for the current path."""
    if (next_i >= len(board) or next_i < 0 or next_j >= len(board[0]) or next_j < 0):
        return False
    return (next_i, next_j) not in path

def _is_word_on_board(board: Board, word: str):
    """Check if the word's characters even appear on the board,
        if they don't appear we don't even need to check them."""
    all_in_board = ''.join((set(char for row in board for char in row)))
    for char in word:
        if (char not in all_in_board):
            return False
    return True

def max_score_paths(board: Board, words: Iterable[str]):
    """Get all the max-score paths on the board, for a given words dictionary.
        A max-score path is determined for each word on the board, having the largest
        path for the specific word."""
    if (isinstance(words, dict)):
        words = words.keys()
    words_on_board = set(filter(lambda word: _is_word_on_board(board, word), words))
    available_paths = _get_paths_for_each_length(board, words_on_board)
    existing_words = set()
    finished_paths: List[Path] = []
    for length in sorted(available_paths.keys(), reverse=True):
        for path in available_paths[length]:
            word = _get_word_from_path(board, path)
            if (word in existing_words):
                continue
            finished_paths.append(path)
            existing_words.add(word)
    return finished_paths

def _get_paths_for_each_length(board: Board, words: Iterable[str]) -> Dict[int, List[Path]]:
    """Get all available paths for each path length, as a dictionary of key-value where
        the key is the path length, and the value is a list of all paths in that length."""
    paths = {}
    words_found: Set[str] = set()
    words_set: Set[str] = set(words)
    for i in range(len(board) ** 2, 0, -1):
        i_paths, words_found = _find_length_n_paths_return_words(i, board, words_set)
        if (len(i_paths) > 0):
            paths[i] = i_paths
            #remove words found - we assume going top to bottom so we always get
            # the highest score for the word first
            words_set.difference_update(words_found)
    return paths

def _find_length_n_paths_return_words(n: int, board: Board, words: Iterable[str]) -> Tuple[List[Path], Set[str]]:
    """"Get all the paths of given length in the given board for a given words dictionary.
        Alongside the paths, return all the words that match those paths."""
    if (isinstance(words, dict)):
        words = words.keys()
    words_on_board = set(filter(lambda word: _is_word_on_board(board, word), words))
    words_found: Set[str] = set()
    paths: List[Path] = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            #start with current cell
            start_path = [(i, j)]
            start_cell = board[i][j]
            start_words = _words_starts_with(words_on_board, board[i][j])
            #add length n paths for current cell
            _find_length_n_paths_return_words_helper(n, board, start_words, words_found, i, j, start_cell, start_path, paths)
    return (paths, words_found)

def _find_length_n_paths_return_words_helper(n: int, board: Board, words: Set[str], words_found: Set[str],
                                             i:int, j: int,curr_word: str, curr_path: Path, finished_paths: List[Path]):
    """Iterate the board, find paths of length n that fit a word in the words set.
        During a spefiic path-trial, filter out words that won't fit."""
    if (len(curr_path) == n):
        #finish case: path length is n
        if (curr_word in words):
            words_found.add(curr_word)
            finished_paths.append(curr_path.copy())
        return
    #prune branches that don't have any words left
    if (len(words) == 0):
        return
    
    for move in OPTIONAL_MOVES:
        next_i = i + move[0]
        next_j = j + move[1]
        if (_safe_to_move(next_i, next_j, board, curr_path)):
            #move forward
            new_word = curr_word + board[next_i][next_j]
            new_path = curr_path + [(next_i, next_j)]
            #filter out words that won't fit current path
            new_words = _words_starts_with(words, new_word)
            _find_length_n_paths_return_words_helper(n, board, new_words, words_found, next_i, next_j,
                                                     new_word, new_path, finished_paths)

def _get_word_from_path(board: Board, path: Path) -> str:
    """Transform given path on a given board to the matching word representation of it."""
    word = ''
    for (i, j) in path:
        word += board[i][j]
    return word