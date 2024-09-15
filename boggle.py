from Game import Game, Difficulty
from boggle_board_randomizer import BOARD_SIZE

TIMER_COUNTDOWN = (3, 0)
DICTIONARY_PATH = "./boggle_dict.txt"

if __name__ == "__main__":
    all_words = set(open(DICTIONARY_PATH).read().splitlines())
    #Change difficulty between EASY/MEDIUM/HARD
    game = Game(BOARD_SIZE, TIMER_COUNTDOWN, all_words, Difficulty.EASY)
    game.start()
