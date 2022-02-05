
from shutil import move


class gameState (): 
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
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
        return self.getAllMoves()

    def getAllMoves(self):
        moves = [] 
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #kollar på första bokstaven av en given pjäs t.ex. bP => b alltså svart pjäs eller -- => - inte en pjäs
                if (turn == "w" and self.whiteMove) or (turn == "b" and not self.whiteMove):
                    piece = self.board[r][c][1] #kollar på andra bokstaven t.ex. om bP => P allstå en bonde
                    if (piece == "P"): 
                        self.getPawnMoves(r,c,moves)
                    elif (piece == "R"):
                        self.getRookMoves(r,c,moves)
                    elif (piece == "N"):
                        self.getNightMoves(r,c,moves)
                    elif (piece == "B"):
                        self.getBishopMoves(r,c,moves)
                    elif (piece == "Q"):
                        self.getQueenMoves(r,c,moves)
                    elif (piece == "K"):
                        self.getKingMoves(r,c,moves)
        return moves

    """
    Get moves for piece located at (r,c) and add to list om possible moves
    """
    def getPawnMoves(self,r,c,moves):
        if (self.whiteMove): #White pawn moves 
            if (self.board[r-1][c] == "--"):
                moves.append(Move((r,c),((r-1),c),self.board))

                if (r == 6) and (self.board[r-2][c]=="--"):
                    moves.append(Move((r,c),((r-2),c),self.board))
            if (c-1 >= 0): 
                if (self.board[r-1][c-1][0] == "b"):
                    moves.append(Move((r,c),((r-1),(c-1)),self.board))
            if(c+1 <= 7):
                if (self.board[r-1][c+1][0] == "b"):
                    moves.append(Move((r,c),((r-1),(c+1)),self.board))
        else: #black pawn moves
            if (self.board[r+1][c]=="--"):
                moves.append(Move((r,c),(r+1,c),self.board))
                if (r == 1) and (self.board[r+2][c]=="--"):
                    moves.append(Move((r,c),(r+2,c),self.board))
            if (c-1>=0):
                if (self.board[r+1][c-1][0]=="w"):
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if (c+1<=7):
                if (self.board[r+1][c+1][0]=="w"):
                    moves.append(Move((r,c),(r+1,c+1),self.board))

    def getRookMoves(self,r,c,moves,dir=((1,0),(0,1),(-1,0),(0,-1))):
        other = "b" if self.whiteMove else "w"

        for d in dir: 
            for i in range(1,8):
                endR = r+d[0]*i
                endC = c+d[1]*i
                if (0 <= endR < 8) and (0 <= endC < 8):
                    p__ = self.board[endR][endC]
                    if (p__ == "--"):
                        moves.append(Move((r,c),(endR,endC),self.board))
                    elif (p__[0] == other):
                        moves.append(Move((r,c),(endR,endC),self.board))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMoves(self,r,c,moves):
        dir = ((1,1),(-1,-1),(1,-1),(-1,1))
        self.getRookMoves(r,c,moves,dir)

    def getQueenMoves(self,r,c,moves):
        dir = ((1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))
        self.getRookMoves(r,c,moves,dir)
   
    def getNightMoves(self,r,c,moves):
        dir = ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1))
        same = "w" if self.whiteMove else "b"

        for d in dir: 
            endR = r + d[0]
            endC = c + d[1]
            if 0 <= endR < 8 and 0 <= endC < 8:
                p__ = self.board[endR][endC]
                if (p__ != same):
                    moves.append(Move((r,c),(endR,endC),self.board))

    def getKingMoves(self,r,c,moves):
        dir = ((1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(-1,1),(1,-1))
        same = "w" if self.whiteMove else "b"

        for i in range(8):
            endR = r+dir[i][0]
            endC = c+dir[i][1]
            if 0 <= endR < 8 and 0 <= endC < 8:
                __p = self.board[endR][endC]
                if (__p[0] != same):
                    moves.append(Move((r,c),(endR,endC),self.board))


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
        self.caputerdPiece = board[self.endR][self.endC]
        self.moveID = self.startR * 1000 + self.startC * 100 + self.endR * 10 + self.endC

    def __eq__(self, __o):
        if isinstance(__o, Move):
            return self.moveID == __o.moveID
        return False
    def getChessNot(self):
        return self.getranktoFile(self.startR,self.startC)+ self.getranktoFile(self.endR,self.endC)

    def getranktoFile(self,r,c):
        return self.colstoFiles[c] + self.rowstoRanks[r]