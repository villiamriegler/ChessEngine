
class gameState (): 
    def __init__(self):
        self.board = [
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["bR","bN","bB","bQ","bK","bB","bN","bR"]
        ]
        self.whiteMove = True
        self.moveLog = []

    def makeMove (self,move): 
        self.board[move.startR][move.startC] = "--"
        self.board[move.endR][move.endC] = move.piceMoved 
        self.moveLog.append(move)
        self.whiteMove = not self.whiteMove

    def undoMove(self):
        if len(self.moveLog) > 0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startR][lastMove.startC] = lastMove.piceMoved 
            self.board[lastMove.endR][lastMove.endC] = lastMove.caputerdPiece
            self.whiteMove = not self.whiteMove

    def getValidMoves(self):
        pass

    def getAllMoves(self):
        pass     


class Move(): 
    rankstoRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCol = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
    colstoFiles = {v:k for k, v in filestoCol.items()}

    def __init__(self,sSq,eSq,board):
        self.startR = sSq[0]
        self.startC = sSq[1]
        self.endR = eSq[0]
        self.endC = eSq[1]        
        
        self.piceMoved = board[self.startR][self.startC]
        print(self.piceMoved)
        self.caputerdPiece = board[self.endR][self.endC]

    def getChessNot(self):
        return self.getranktoFile(self.startR,self.startC)+ self.getranktoFile(self.endR,self.endC)

    def getranktoFile(self,r,c):
        return self.colstoFiles[c] + self.rowstoRanks[r]