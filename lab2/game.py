from constants import BOARD_SIZE, WHITE, BLACK, EMPTY, DIRECTIONS

class Game:

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.current_player = self.player_1
        self.initialize_board()

    def initialize_board(self):
        self.board = [[' '] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[3][3] = self.player_1.color
        self.board[4][4] = self.player_1.color
        self.board[3][4] = self.player_2.color
        self.board[4][3] = self.player_2.color
        return self.board

    # Display the game self.board
    def display_board(self):
        print('   a b c d e f g h')
        print('  -----------------')
        for i in range(BOARD_SIZE):
            print(f'{i+1}|', end=' ')
            for j in range(BOARD_SIZE):
                print(self.board[i][j], end=' ')
            print(f'|{i+1}')
        print('  -----------------')
        print('   a b c d e f g h')

    def count_discs(self):
        player_1_count, player_2_count = 0, 0

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == self.player_1.color:
                    player_1_count += 1
                elif self.board[row][col] == self.player_2.color:
                    player_2_count += 1
        return player_1_count, player_2_count

    # Get the opponent's color
    def get_opponent_color(self, player):
        if player.color == self.player_1.color:
            return self.player_2.color
        else:
            return self.player_1.color

    # Check if a move is valid
    def get_valid_directions(self, row, col, player):
        valid_directions = []
        if self.board[row][col] != EMPTY:
            return []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and self.board[r][c] == self.get_opponent_color(player):
                while r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and self.board[r][c] == self.get_opponent_color(player):
                    r += dr
                    c += dc
                if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and self.board[r][c] == player.color:
                    valid_directions.append((dr, dc))
        return valid_directions

    # Get a list of all valid moves for a player
    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                valid_directions = self.get_valid_directions(row, col, player)
                if len(valid_directions) > 0:
                    valid_moves.append((row, col, valid_directions))
        return valid_moves
    
    def flip_disc(self, row, column, color):
        self.board[row][column] = color

    def flip_discs(self, row, col, valid_directions, player):
        self.flip_disc(row, col, player.color)
        for dr, dc in valid_directions:
            r, c = row + dr, col + dc
            if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and self.board[r][c] == self.get_opponent_color(player):
                while r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and self.board[r][c] == self.get_opponent_color(player):
                    self.flip_disc(r, c, player.color)
                    r += dr
                    c += dc
    
    def process_move(self, player):
        valid_moves = self.get_valid_moves(player)

        if len(valid_moves) == 0:
            player.forfeit = True
            return
        
        player.forfeit = False

        while True:
            move = player.make_move(valid_moves, self)
            if self.perform_move(player, move, valid_moves):
                break

        return move
    
    def perform_move(self, player, move, valid_moves):
        if move in list(map(lambda t: (t[0], t[1]), valid_moves)):
            row, col = move
            directions = list(filter(lambda t: t[0] == row and t[1] == col, valid_moves))[0][2]
            self.flip_discs(row, col, directions, player)
            return True
        
        return False
        

    def is_game_finished(self):
        return self.player_1.forfeit and self.player_2.forfeit
    
    def switch_players(self):
        if self.current_player == self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1

    def start(self):
        while not self.is_game_finished():
            self.display_board()
            print("{} player turn to move".format(self.current_player.name))
            self.process_move(self.current_player)
            self.switch_players()

        player_1_count, player_2_count = self.count_discs()
        print("{} score: {}, \n{} score: {}".format(self.player_1.name, player_1_count, self.player_2.name, player_2_count))
