from player import Player

class HumanPlayer(Player):

    def make_move(self, valid_moves, game):
        valid_moves = list(map(lambda m: str(chr(m[1] + ord('a'))) + str(m[0] + 1), valid_moves))
        print("Valid moves: {}".format(str(valid_moves)))
        while True:
            move = input('Enter your move (e.g. "d3"): ')
            if len(move) == 2:
                row = int(move[1]) - 1
                col = ord(move[0]) - ord('a')
                return row, col
