class gameState (): 
    def __init__(self):
        self.board = [
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            ["wP","wP","wP","wP","wP","wP","wP","wP"]
            ["--","--","--","--","--","--","--","--"]
            ["--","--","--","--","--","--","--","--"]
            ["--","--","--","--","--","--","--","--"]
            ["--","--","--","--","--","--","--","--"]
            ["bP","bP","bP","bP","bP","bP","bP","bP"]
            ["bR","bN","bB","bQ","bK","bB","bN","bR"]]
        self.whiteMove = True
        self.moveLog = []