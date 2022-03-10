from asyncio.windows_events import NULL
import random
from socket import SocketIO

pieceVal = {"K":0, "Q":9, "R":5, "B":3, "N":3, "P":1}
Checkmate = 1000
Stalemate = 0
DEPTH = 3

"""
Picks a random move
"""
def findRandMove (validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

"""
Find the best move 
"""
def findMove (gs,validMoves):
    turn = 1 if gs.whiteMove else -1

    oppMinMaxScore = Checkmate #our best possible score
    Move = None

    random.shuffle(validMoves)
    for m in validMoves: #Looping thru all valid moves 
        gs.makeMove(m) #make thge move 
        opponetsMoves = gs.getValidMoves() #get opponents responses 
        if gs.staleMate:
            oppMaxScore = Stalemate
        elif gs.checkMate:
            oppMaxScore = -Checkmate
        else:
            oppMaxScore = -Checkmate #opponents best possible score
            for opponentsMove in opponetsMoves: 
                gs.makeMove(opponentsMove) #make all opponents moves 
                gs.getValidMoves() #updating checkmate
                if gs.checkMate:
                    score = Checkmate
                elif gs.staleMate:
                    score = Stalemate
                else:
                    score = -turn * matScore(gs.board) #Scoring the board 
                if score > oppMaxScore: #if the score if better for us uppdate opponets best score 
                    oppMaxScore = score
                gs.undoMove()

        if oppMaxScore < oppMinMaxScore: #if oppents best score is less then, our best score uppdate our best score. (Presume opponent plays opimaly)
            oppMinMaxScore = oppMaxScore
            Move = m 
        gs.undoMove()
    
    return Move


"""
Helper to make first recursive call to findMinMaxMove
"""
def findBestMove(gs,validMoves):
    global nextMove
    nextMove = None
    findMinMaxMove(gs,validMoves,gs.whiteMove,DEPTH)
    return nextMove

def findMinMaxMove(gs,validMoves,whiteMove,depth):
    global nextMove
    if depth == 0: 
        return scoreBoard(gs)
    
    if whiteMove:
        maxScore = -Checkmate
        for m in validMoves:
            gs.makeMove(m)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs,nextMoves,False,depth-1)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = m
            gs.undoMove()
        return maxScore

    else:
        minScore = Checkmate
        for m in validMoves:
            gs.makeMove(m)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs,nextMoves,True,depth-1)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = m
            gs.undoMove()
        return minScore

def scoreBoard(gs):  
    #white wants as big a number as possible and vice versa
    if gs.checkMate:
        if gs.whiteMove:
            return -Checkmate #black wins
        else:
            return Checkmate
    elif gs.staleMate:
        return Stalemate

    score = 0  
    for r in gs.board:
        for c in r:
            if c[0] == "w":
                score += pieceVal[c[1]]
            elif c[0] == "b":
                score -= pieceVal[c[1]]
    return score 


"""
Apply score to board based on material
"""
def matScore(board):
    score = 0 #white wants as big a number as possible and vice versa 
    for r in board:
        for c in r:
            if c[0] == "w":
                score += pieceVal[c[1]]
            elif c[0] == "b":
                score -= pieceVal[c[1]]
    return score 
