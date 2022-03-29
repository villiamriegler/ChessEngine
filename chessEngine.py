from re import T
from shutil import move


class gameState (): 
    def __init__(self):
        #Setting up the board with all pieces
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
        #Keping track of whose tur it is and the moves made 
        self.whiteMove = True
        self.moveLog = []

        #Keeping tack of kings for checks, pins, stalemates and, checkmates
        self.wKLoc = (7,4) #Starting positions
        self.bKLoc = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False

        #en passant
        self.enpassandt = () #coords for sq where en passant is possible

        #castle rights
        self.currentCastleRights = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(True,True,True,True)]

    """
    Function for moving a piece from one location to the next [doesn't check if move is valid at all]
        Args: Move object containing starting pos and ending pos and the pieces already on those squares
    """
    def makeMove (self,move): 
        #emptys the starting position of the moving piece 
        self.board[move.startR][move.startC] = "--"
        
        #places the moving piece on the new square 
        self.board[move.endR][move.endC] = move.piceMoved 
        
        #appends to the movelog and switches turn
        self.moveLog.append(move)
        self.whiteMove = not self.whiteMove

        #uppdating location of kings
        if (move.piceMoved == "wK"):
            self.wKLoc = (move.endR,move.endC)
        elif (move.piceMoved == "bK"):
            self.bKLoc = (move.endR,move.endC)

        #Pawn Promotion
        if move.isPawnProm:
            self.board[move.endR][move.endC] = move.piceMoved[0] + "Q"

        #En Passant
        if move.isEnpassantMove:
            self.board[move.startR][move.endC] = "--" #capturing the pawn
        if move.piceMoved[1] == "P" and abs(move.startR - move.endR) == 2: #uppdate enpassant variable 
            self.enpassandt = ((move.startR + move.endR)//2 , move.endC)
        else:
            self.enpassandt = ()

        #castle moveing the rook
        if move.castle:
            if move.endC - move.startC == 2: #king side castle
                self.board[move.endR][move.endC-1] = self.board[move.endR][move.endC+1]
                self.board[move.endR][move.endC+1] = "--"
            else: #queen side castle
                self.board[move.endR][move.endC+1] = self.board[move.endR][move.endC-2]
                self.board[move.endR][move.endC-2] = "--"

        #uppdate casteling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRights.wks,self.currentCastleRights.bks,
                                                    self.currentCastleRights.wqs,self.currentCastleRights.bqs))

    """
    Function for unding the last move
        uses the self.moveLog to replace a captured piece and place back the caputing piece 
    """
    def undoMove(self):
        #Checking so that a move has actually been made 
        if len(self.moveLog) > 0:
            #same as move function only uses a previous move object
            lastMove = self.moveLog.pop()
            self.board[lastMove.startR][lastMove.startC] = lastMove.piceMoved 
            self.board[lastMove.endR][lastMove.endC] = lastMove.caputerdPiece
            self.whiteMove = not self.whiteMove

        #uppdating location of kings
        if (lastMove.piceMoved == "wK"):
            self.wKLoc = (lastMove.startR,lastMove.startC)
        elif (lastMove.piceMoved == "bK"):
            self.bKLoc = (lastMove.startR,lastMove.startC)

        #en passant 
        if lastMove.isEnpassantMove:
            self.board[lastMove.endR][lastMove.endC] = "--"
            self.board[lastMove.startR][lastMove.endC] = lastMove.caputerdPiece
            self.enpassandt = (lastMove.endR,lastMove.endC)
        #undo a 2 sq pawn advance 
        if lastMove.piceMoved[1] == "P" and abs(lastMove.startR - lastMove.endR) == 2:
            self.enpassandt = ()

        #casteling
        self.currentCastleRights = self.castleRightsLog[len(self.castleRightsLog)-1] #set current castlerights to the new last of the list
        self.castleRightsLog.pop(-1) #get rid of new castlerights 
        
        #undo castle move
        if lastMove.castle:
            if lastMove.endC - lastMove.startC == 2: #kingside
                self.board[lastMove.endR][lastMove.endC+1] = self.board[lastMove.endR][lastMove.endC-1]
                self.board[lastMove.endR][lastMove.endC-1] = "--"
            else:
                self.board[lastMove.endR][lastMove.endC-2] = self.board[lastMove.endR][lastMove.endC+1]
                self.board[lastMove.endR][lastMove.endC+1] = "--"

        self.checkMate = False
        self.staleMate = False

    def updateCastleRights(self,move):
        if move.piceMoved == "wK":
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.piceMoved == "bK":
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.piceMoved == "wR":
            if move.startR == 7:
                if move.startC == 0: #left rook
                    self.currentCastleRights.wqs = False
                elif move.startC == 7: #right rook
                    self.currentCastleRights.wks = False
        elif move.piceMoved == "bR":
            if move.startR == 0:
                if move.startC == 0: #left rook
                    self.currentCastleRights.bqs = False
                elif move.startC == 7: #right rook
                    self.currentCastleRights.bks = False



    """
    All moves considering checks, pins and so on
    """
    def getValidMoves(self):
        moves = []
        self.inCheck , self.pins, self.checks = self.checkPinsAndChecks()
        if self.whiteMove:
            kr = self.wKLoc[0]
            kc = self.wKLoc[1]
        else:
            kr = self.bKLoc[0]
            kc = self.bKLoc[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllMoves()
                c = self.checks[0]
                cr = c[0]
                cc = c[1]
                cP = self.board[cr][cc]
                validSQ = []
                if cP[1] == 'N':
                    validSQ = [(cr,cc)]
                else: 
                    for i in range(1,8):
                        _validSQ = (kr + c[2] * i, kc + c[3] * i)
                        validSQ.append(_validSQ)
                        if _validSQ[0] == cr and _validSQ[1] == cc:
                            break

                for i in range(len(moves)-1,-1,-1):
                    if moves[i].piceMoved[1] != 'K':
                        if not (moves[i].endR, moves[i].endC) in validSQ:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kr,kc,moves)
        else:
            moves = self.getAllMoves()

        return moves


    def checkPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteMove:
            otherC = "b"
            allyC = "w"
            sr = self.wKLoc[0]
            sc = self.wKLoc[1]
        else:
            otherC = "w"
            allyC = "b"
            sr = self.bKLoc[0]
            sc = self.bKLoc[1]
        
        dir = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(dir)):
            d = dir[j]
            _pins = ()
            for i in range(1,8):
                endr = sr + d[0] * i
                endc = sc + d[1] * i
                if 0 <= endr < 8 and 0 <= endc < 8:
                    endP = self.board[endr][endc]
                    if endP[0] == allyC:
                        if _pins == ():
                            _pins = (endr,endc,d[0],d[1])
                        else:
                            break
                    elif endP[0] == otherC:
                        type = endP[1]

                        if (0<=j <= 3 and type == 'R') or \
                            (4<= j <=7 and type =='B') or \
                            (i == 1 and type == 'P' and ((otherC == 'w' and 6 <= j <= 7) or (otherC == 'b' and 4 <= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if _pins == ():
                                inCheck = True
                                checks.append((endr,endc,d[0],d[1]))
                                break
                            else:
                                pins.append(_pins)
                                break
                        else:
                            break
                else:
                    break
        knightDir = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightDir:
            endr = sr + m[0]
            endc = sc + m[1]
            print((endr,endc))
            if 0 <= endr <= 7 and 0 <= endc <= 7:
                endP = self.board[endr][endc]
                if endP[0] == otherC and endP[1] == 'N':
                    inCheck = True 
                    checks.append((endr,endc,m[0],m[1]))

        return inCheck , pins , checks 


    """
    Check if current player is in check
    """
    def inCheck(self):
        if (self.whiteMove): #checking if the square under attack is the white of black king
            return self.sqUnderAttack(self.wKLoc[0],self.wKLoc[1])
        else: 
            return self.sqUnderAttack(self.bKLoc[0],self.bKLoc[1])

    """
    Check if the enemy can attack (r,c)
    """
    def sqUnderAttack(self,r,c):
        self.whiteMove = not self.whiteMove #switching turns 
        opponentMoves = self.getAllMoves()
        for move in opponentMoves:
            if (move.endR == r and move.endC == c): #checking if the square is under attack
                self.whiteMove = not self.whiteMove #switching back moves
                return True
            
        self.whiteMove = not self.whiteMove
        return False

    """
    Gets all valid moves acording to how the pieces are alowed to move [ignores checks, pins and so on]
    """
    def getAllMoves(self):
        moves = [] #stores all valid moves 
        
        #loops thru all rows and colums of the board 
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #checks the color of the moving piece 
                if (turn == "w" and self.whiteMove) or (turn == "b" and not self.whiteMove):
                    piece = self.board[r][c][1] #Checks the kind of piece 
                    
                    #running the right function for the right piece type 
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
    Get moves for piece located at (r,c) and add to list of possible moves
    """
    def getPawnMoves(self,r,c,moves):
        if (self.whiteMove): #White pawn moves 
            if (self.board[r-1][c] == "--"): #Cheking if the square infront is empty and if the pawn is in starting pos if the two squares infron are empty
                moves.append(Move((r,c),((r-1),c),self.board))
                if (r == 6) and (self.board[r-2][c]=="--"):
                    moves.append(Move((r,c),((r-2),c),self.board))
            
            #Checks diagonals for captures
            if (c-1 >= 0): 
                if (self.board[r-1][c-1][0] == "b"):
                    moves.append(Move((r,c),((r-1),(c-1)),self.board))
                elif ((r-1,c-1) == self.enpassandt): #logic for enpassant captures
                    moves.append(Move((r,c),((r-1),(c-1)),self.board,enpassantPossible=True))
            if(c+1 <= 7):
                if (self.board[r-1][c+1][0] == "b"):
                    moves.append(Move((r,c),((r-1),(c+1)),self.board))
                elif ((r-1,c+1) == self.enpassandt):
                    moves.append(Move((r,c),((r-1),(c+1)),self.board,enpassantPossible=True))
        
        else: #black pawn moves
            if (self.board[r+1][c]=="--"):
                moves.append(Move((r,c),(r+1,c),self.board))
                if (r == 1) and (self.board[r+2][c]=="--"):
                    moves.append(Move((r,c),(r+2,c),self.board))
            if (c-1>=0):
                if (self.board[r+1][c-1][0]=="w"):
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif ((r+1,c-1) == self.enpassandt):
                    moves.append(Move((r,c),((r+1),(c-1)),self.board,enpassantPossible=True))
            if (c+1<=7):
                if (self.board[r+1][c+1][0]=="w"):
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif ((r+1,c+1) == self.enpassandt):
                    moves.append(Move((r,c),((r+1),(c+1)),self.board,enpassantPossible=True))

    def getRookMoves(self,r,c,moves,dir=((1,0),(0,1),(-1,0),(0,-1))):
        #defining the oposposing teams color
        other = "b" if self.whiteMove else "w"

        #looping thru the directions to check, for a roock we check up,down,left,right 
        for d in dir: 
            for i in range(1,8): #Loping thru the lenght of the board 
                endR = r+d[0]*i #takes the starting pos and loops thur each next square in given direction 
                endC = c+d[1]*i
                if (0 <= endR < 8) and (0 <= endC < 8): #If you hit the end of the board 
                    p__ = self.board[endR][endC]
                    if (p__ == "--"): #If there is nothing in the way -> add that move 
                        moves.append(Move((r,c),(endR,endC),self.board))
                    elif (p__[0] == other): #If there is an enemy in the way add that move and break the loop 
                        moves.append(Move((r,c),(endR,endC),self.board))
                        break
                    else: #if there is a friendly in the way break the loop
                        break
                else:
                    break

    def getBishopMoves(self,r,c,moves):
        #A bishop works as a rook moving in different directions, we check all diagonals
        dir = ((1,1),(-1,-1),(1,-1),(-1,1))
        self.getRookMoves(r,c,moves,dir)

    def getQueenMoves(self,r,c,moves):
        #Works as a combination of a rook and a bishop
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
   
    def getNightMoves(self,r,c,moves):
        dir = ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)) #list of all different jumps a night can do relative to its current pos 
        same = "w" if self.whiteMove else "b" #defining friendly pieces 

        for d in dir: #loping thru jumps
            endR = r + d[0] #finding the end point of that jump
            endC = c + d[1]
            if 0 <= endR < 8 and 0 <= endC < 8: #checking so we don't jump out of the playing field
                p__ = self.board[endR][endC] #looking whats on the landing square 
                if (p__[0] != same): #If its not a friendy add the move
                    moves.append(Move((r,c),(endR,endC),self.board))

    def getKingMoves(self,r,c,moves):
        dir = ((1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(-1,1),(1,-1)) #All relative steps a king can take 
        same = "w" if self.whiteMove else "b" #Defing same colored pieces 

        for i in range(8):
            endR = r+dir[i][0]#Getting end position of a step
            endC = c+dir[i][1]
            if (0 <= endR < 8 and 0 <= endC < 8): #keeping within the board 
                __p = self.board[endR][endC]
                if (__p[0] != same): #if not friendly, add the move 
                    moves.append(Move((r,c),(endR,endC),self.board))

    """
    generate valid casteling moves
    """
    def getCastleMoves(self,r,c,moves):
        if self.sqUnderAttack(r,c):
            return
        if (self.whiteMove and self.currentCastleRights.wks) or (not self.whiteMove and self.currentCastleRights.bks):
            self.getKsCastleMoves(r,c,moves)
        if (self.whiteMove and self.currentCastleRights.wqs) or (not self.whiteMove and self.currentCastleRights.bqs):
            self.getQsCastleMoves(r,c,moves)
        
    def getKsCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.sqUnderAttack(r,c+1) and not self.sqUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,castle = True))

    def getQsCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.sqUnderAttack(r,c-1) and not self.sqUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,castle = True))

class Move(): 
    #converting rows and columns to chess notation 
    rankstoRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCol = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
    colstoFiles = {v:k for k, v in filestoCol.items()}

    def __init__(self,sSq,eSq,board,enpassantPossible = False, castle = False):
        #start and end pos of the move
        self.startR = sSq[0]
        self.startC = sSq[1]
        self.endR = eSq[0]
        self.endC = eSq[1]        
        
        #effected pieces by the move
        self.piceMoved = board[self.startR][self.startC]
        self.caputerdPiece = board[self.endR][self.endC]

        #Pawn promotions
        self.isPawnProm = False
        if (self.piceMoved == "wP" and self.endR == 0) or (self.piceMoved == "bP" and self.endR == 7):
            self.isPawnProm = True

        #En passant
        self.isEnpassantMove = False
        if (enpassantPossible):
            self.isEnpassantMove = True
        if self.isEnpassantMove:
            self.caputerdPiece = "wP" if self.piceMoved == "bP" else "bP"

        #casteling
        self.castle = castle
        
        #Id for the move (maybe useful for recreating old positions in the future)
        self.moveID = self.startR * 1000 + self.startC * 100 + self.endR * 10 + self.endC

    def __eq__(self, __o):
        #Overwriting the equals sign
        if isinstance(__o, Move):
            return self.moveID == __o.moveID
        return False
    
    """
    Converting a move to chess notation
    """
    def getChessNot(self):
        return self.getranktoFile(self.startR,self.startC)+ self.getranktoFile(self.endR,self.endC)

    def getranktoFile(self,r,c):
        return self.colstoFiles[c] + self.rowstoRanks[r]

class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        