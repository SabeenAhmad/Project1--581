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


        