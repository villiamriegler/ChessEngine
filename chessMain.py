from math import fabs
import pygame 
from chessEngine import *


#Skärm variabler 
width = height = 512
dim = 8 
sqSize = width//dim 
maxFps = 24 

"""
Loads all images and saves them in a dictionary 
"""
#Dict för alla pjäser så att de slipper laddas fler gånger 
images = {}
def loadImgs(): 
    pieces = ["wR","wN","wB","wQ","wK","wB","wN","wR","bR","bN","bB","bQ","bK","bB","bN","bR","wP","bP"]

    for p in pieces:
        images[p] = pygame.transform.scale(pygame.image.load("images/"+p+".png"),(sqSize,sqSize))


"""
Ritar all grafik för den nuvarande positionen på skärmen
"""
def drawGs(screen,gs,sqSelected,validMoves):
    drawSq(screen)
    hightlightSq(screen,validMoves,sqSelected,gs)
    drawPieces(screen, gs.board)

def drawSq(screen):
    colors = [pygame.Color("gray"),pygame.Color("dark gray")]
    for r in range(dim): #loop for drawing the background and highligting pressed pieces
        for c in range(dim):
            color = (r+c)%2
            pygame.draw.rect(screen, colors[color], pygame.Rect(c*sqSize,r*sqSize,sqSize,sqSize))

def drawPieces(screen,board):
    for r in range(dim): #Draws all the pieces on the board
        for c in range(dim):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(images[piece],pygame.Rect(c*sqSize,r*sqSize,sqSize,sqSize))


def hightlightSq(screen,validMoves,sqSelected,gs):  
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteMove else "b"): #only highlights if it's the right pice to move
            s = pygame.Surface((sqSize,sqSize))
            s.set_alpha(255)
            s.fill(pygame.Color("green"))
            screen.blit(s,(c*sqSize,r*sqSize)) #highlights selected square
            for m in validMoves: #highlights valid moves
                if m.startR == sqSelected[0] and m.startC == sqSelected[1]:
                    s.fill(pygame.Color("light green"))
                    screen.blit(s,(m.endC*sqSize,m.endR*sqSize))


"""
Handeling player input
"""
def playerMove(gs,validMoves,sqSelected,playerClicks = []):
    mouseLocation = pygame.mouse.get_pos() #gets mouse location on screen and converts to rows and columns
    c = mouseLocation[0]//sqSize
    r = mouseLocation[1]//sqSize
    if sqSelected == (r,c): #If the same square clicked twice cancel the move 
        sqSelected = ()
        playerClicks.clear()
        return (False,sqSelected)
    else: #Appending the second click 
        sqSelected = (r,c)
        playerClicks.append(sqSelected)
    if len(playerClicks) == 2: #if there are two clicks in player clicks, do a move 
        move = Move(playerClicks[0], playerClicks[1], gs.board) #definging the move
        for i in range(len(validMoves)):
            if move == validMoves[i]: #checks if the move is vaild 
                gs.makeMove(validMoves[i])
                sqSelected = () #emptys the click variables 
                playerClicks.clear()
                return (True,sqSelected)
        
        playerClicks.clear()
        playerClicks = [sqSelected]
        sqSelected = ()
    return (False,sqSelected)


def main():
    #initialisation 
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    
    #gets the gamestate and checks for valid moves in the starting pos
    gs = gameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    sqSelected = ()
     
    #variabler till spelloopen
    loadImgs() #Gör bara en gång 
    run = True
    while run: 
        for e in pygame.event.get(): #loop for getting event handelers
            #Kryssa ner spelet
            if e.type == pygame.QUIT: 
                run = False
            #undo move
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True
            #Flyttar en pjäs        
            elif e.type == pygame.MOUSEBUTTONDOWN:
                moveandsq = playerMove(gs,validMoves,sqSelected)
                moveMade = moveandsq[0]
                sqSelected = moveandsq[1]   
        
        if moveMade: #if a valid move was made get all new moves
            validMoves = gs.getValidMoves()
            moveMade = False 
            sqSelected = () 

        #Draws the screen
        drawGs(screen,gs,sqSelected,validMoves)
        clock.tick(maxFps)
        pygame.display.flip()

if __name__ == "__main__":
    main()