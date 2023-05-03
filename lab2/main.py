from game import Game
from human_player import HumanPlayer
from ai_player_alpha_beta import AIPlayerAlphaBeta, joined_heuristic
from ai_player import AIPlayer
from constants import WHITE, BLACK
import time

def main():
    player_1 = AIPlayer("WHITE", WHITE, joined_heuristic, 1)
    player_2 = AIPlayer("BLACK", BLACK, joined_heuristic, 3)
    game = Game(player_1, player_2)
    start_time = time.time()
    game.start()
    print("Players: ")
    print(player_1.name + ", depth:" + str(player_1.max_depth) + " alpha beta:" + str(type(player_1) == AIPlayerAlphaBeta))
    print(player_2.name + ", depth:" + player_2.max_depth + " alpha beta:" + str(type(player_2) == AIPlayerAlphaBeta))
    print("Time:")
    print(time.time() - start_time)

if __name__ == "__main__":
    main()