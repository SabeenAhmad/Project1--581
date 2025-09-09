from board import Board
from ui import UI

class Game:
    def __init__(self, mine_total=10):
        self.playing_state = "PLAYING"   # can be "PLAYING", "WON", "LOST"
        self.board = Board(mine_total)

def main():
    # make game + ui
    game = Game(mine_total=10)   # adjust number of mines if you want
    ui = UI(game, game.board)

    # start game
    ui.start_screen()

if __name__ == "__main__":
    main()
