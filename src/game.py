from board import Board

class Game:
    def __init__(self, mine_total):
        self.playing_state = "PLAYING"   # can be "PLAYING", "WON", "LOST"
        self.board = Board(mine_total)

