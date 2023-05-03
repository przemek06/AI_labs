from constants import BOARD_SIZE, WHITE, BLACK, EMPTY, DIRECTIONS

class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.forfeit = False


    def make_move(self, valid_moves, game):
        pass