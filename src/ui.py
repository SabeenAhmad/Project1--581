# UI file

class UI: 
    def __init__(self, game, board):
        self.game = game # Stores a reference to the Game object so game.py can be reached.
        self.board = board # Stores a reference to the Board object so board.py can be reached.

    def start_screen(self):
        input("=== Welcome to Minesweeper ===\nPress ENTER to start...")
        self.game_loop()

    def game_loop(self):
        print("\n--- Game started! ---")
        self.board.print_board(self.game.playing_state)

    '''
    def end_screen(): 

    def render_game(): 

    def render_status(): 

    def render_board(): 

    def ask_for_input(): 
    '''
