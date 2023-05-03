from constants import BOARD_SIZE, WHITE, BLACK, EMPTY, DIRECTIONS
from player import Player
import copy

weights = [
        [60, -20,  20,   5,   5,  20, -20, 60],
        [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
        [ 20,  -5,  15,   3,   3,  15,  -5,  20],
        [  5,  -5,   3,   3,   3,   3,  -5,   5],
        [  5,  -5,   3,   3,   3,   3,  -5,   5],
        [ 20,  -5,  15,   3,   3,  15,  -5,  20],
        [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
        [60, -20,  20,   5,   5,  20, -20, 60]
    ]

def end_score_heuristic(player, game):
    if player.name == game.player_1.name:
            return game.count_discs()[0]
    return game.count_discs()[1]

def tiles_score_heuristic(player, game):
    score = 0
    board = game.board

    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == player.color:
                score = score + weights[i][j]

    return score

def number_of_moves_heurisitc(player, game):
    return len(game.get_valid_moves(player))

def joined_heuristic(player, game):
    score = end_score_heuristic(player, game)*16 + tiles_score_heuristic(player, game) + number_of_moves_heurisitc(player, game)*16
    return score

class AIPlayerAlphaBeta(Player):

    def __init__(self, name, color, heuristic, max_depth):
        super().__init__(name, color)
        self.heuristic = heuristic
        self.max_depth = max_depth

    def make_move(self, valid_moves, game):
        scores = []
        for move in valid_moves:
            move_to_consider = (move[0], move[1])
            game_clone = self.replicate_game(game)
            game_clone.perform_move(game_clone.current_player, move_to_consider, valid_moves)
            game_clone.switch_players()
            new_valid_moves = game_clone.get_valid_moves(game_clone.current_player)
            score = self.minimax(new_valid_moves, game_clone, 0, float("-inf"), float("inf"))
            scores.append(score)

        max_index = scores.index(max(scores))
        return valid_moves[max_index][0], valid_moves[max_index][1]

    def minimax(self, valid_moves, game, depth, alpha, beta):

        isMin = self.name == game.current_player.name
        
        if game.is_game_finished() or depth == self.max_depth or len(valid_moves) == 0:
            return self.heuristic(self, game)

        end_score = float("inf") if isMin else float("-inf")
        
        for move in valid_moves:
            game_clone = self.replicate_game(game)
            move_to_consider = (move[0], move[1])
            moved = game_clone.perform_move(game_clone.current_player, move_to_consider, valid_moves)
            if not moved:
                print("error")
            game_clone.switch_players()
            valid_moves_t = game_clone.get_valid_moves(game_clone.current_player)
            score = self.minimax(valid_moves_t, game_clone, depth + 1, alpha, beta)
            if isMin:
                end_score = min(score, end_score)
                beta = min(beta, end_score)
                if alpha >= beta:
                    return beta
            else:
                end_score = max(score, end_score)
                alpha = max(alpha, end_score)
                if alpha >= beta:
                    return alpha

        return end_score




    def replicate_game(self, game):
        return copy.deepcopy(game)
