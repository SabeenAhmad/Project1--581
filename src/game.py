'''
Game Class
'''
from board import Board
class Game:
    #initializing Game
    def __init__ (self, mines_total):
        '''
        initializing Game using user input for mine total
        '''
        self.playing_state = 'PLAYING'
        self.mine_total = mines_total
        self.mine_count = 0
        self.flags_remaining = mines_total
        self.board = Board(self.mine_total)
        self.first_move = True
        self.start_screen()
    
    def start_screen(self):
        input("=== Welcome to Minesweeper ===\nPress ENTER to start...")
        self.game_loop()
    def game_loop(self):
        print("\n--- Game started! ---")
        self.board.print_board(self.playing_state)
    
    def toggle_flag(self, r, c):
        if not self.board.in_bounds(r, c):
            return 'INVALID'

        cell_state = self.board.state[r][c]

        # cannot flag an uncovered cell
        if cell_state == 'UNCOVERED':
            return 'INVALID'

        # unflag
        if cell_state == 'FLAG':
            self.board.state[r][c] = 'COVERED'
            self.flags_remaining += 1
            return 'UNFLAGGED'
        
        # place flag
        if self.flags_remaining == 0:
            return 'NO_FLAGS'

        self.board.state[r][c] = 'FLAG'
        self.flags_remaining -= 1
        return 'FLAGGED'
            