'''
Game Class
'''
from board import Board
from ui import UI

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
  
        # Moved UI files to ui.py class and made a class in that ui.py so we can call upon methods defined there. 
        self.ui = UI(self, self.board)
        self.ui.start_screen()
 
