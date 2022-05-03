from asyncio.windows_events import NULL
from audioop import reverse
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
    validMoves = moveOrder(validMoves)
    findNegaMaxMoveAlphaBeta(gs,validMoves,DEPTH,-Checkmate,Checkmate,1 if gs.whiteMove else -1)
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

def findNegaMaxMove(gs,validMoves,depth,turnMultip):
    global nextMove
    if depth == 0:
       return turnMultip * scoreBoard(gs)

    maxscore = -Checkmate
    for m in validMoves:
        gs.makeMove(m)
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxMove(gs, nextMoves, depth-1,-turnMultip)
        if score > maxscore:
            maxscore = score
            if depth == DEPTH:
                nextMove = m
        gs.undoMove()

    return maxscore

def findNegaMaxMoveAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultip):
    global nextMove
    if depth == 0:
       return turnMultip * scoreBoard(gs)   

    maxscore = -Checkmate
    for m in validMoves:
        gs.makeMove(m)
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxMoveAlphaBeta(gs, nextMoves, depth-1,-beta,-alpha,-turnMultip)
        if score > maxscore:
            maxscore = score
            if depth == DEPTH:
                nextMove = m
        gs.undoMove()

        #pruning
        if maxscore > alpha:
            alpha = maxscore
        if alpha >= beta:
            break

    return maxscore

def moveOrder(moves):
    moves.sort(key=lambda x:x.caputerdPiece != "--",reverse=True) 
    return moves

def scoreBoard(gs):  
    #white wants as big a number as possible and vice versa
    if gs.checkMate:
        if gs.whiteMove:
            return -Checkmate #black wins
        else:
            return Checkmate
    elif gs.staleMate:
        return Stalemate

    score = matScore(gs.board) + developmentScore(gs.board)
    return score 


"""
Apply score to board based on material
"""
def matScore(board):
    score = 0 #white wants as big a number as possible and vice versa
    BplacenemtScore = 0 
    WplacenemtScore = 0
    devScore = 0
    for r in board:
        for c in r:
            if c[0] == "w":
                score += pieceVal[c[1]]
                devScore -= WplacenemtScore 
            elif c[0] == "b":
                score -= pieceVal[c[1]]
                devScore += BplacenemtScore

        if BplacenemtScore <= 0.5:
            BplacenemtScore += 0.1
            if BplacenemtScore == 0.3:
                WplacenemtScore = 0.5
        if WplacenemtScore > 0:
            WplacenemtScore -= 0.1
        
    return score + devScore * 0.1

def developmentScore(board): 
    score = 0
    placenemtScore = 0
    for r in board:
        for c in r:
            if c[0] == "w":
                score += pieceVal[c[1]] * -placenemtScore
            elif c[0] == "b":
                score -= pieceVal[c[1]] * placenemtScore
        if placenemtScore < 0.5:
            placenemtScore += 0.1

    return score * 0.1