import pygame 
from chessEngine import *


#Skärm variabler 
width = height = 512
dim = 8 
sqSize = width//dim 
maxFps = 24 

#Dict för alla pjäser så att de slipper laddas fler gånger 
images = {}

def loadImgs(): 
    """
    Laddar in bilderna för alla pjäser och sätter in dem i ett dict 
    """
    pieces = ["wR","wN","wB","wQ","wK","wB","wN","wR","bR","bN","bB","bQ","bK","bB","bN","bR","wP","bP"]

    for p in pieces:
        images[p] = pygame.transform.scale(pygame.image.load("images/"+p+".png"),(sqSize,sqSize))




def drawGs(screen,gs,sqSelected):
    """
    Ritar all grafik för den nuvarande positionen på skärmen
    """
    drawSq(screen,sqSelected,gs)
    drawPieces(screen, gs.board)

def drawSq(screen,sqSelected,gs):
    colors = [pygame.Color("gray"),pygame.Color("dark gray")]
    for r in range(dim):
        for c in range(dim):
            color = (r+c)%2
            if sqSelected == (r,c):
                pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(c*sqSize,r*sqSize,sqSize,sqSize))  
            else: 
                pygame.draw.rect(screen, colors[color], pygame.Rect(c*sqSize,r*sqSize,sqSize,sqSize))

def drawPieces(screen,board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(images[piece],pygame.Rect(c*sqSize,r*sqSize,sqSize,sqSize))




def main():
    #initialisation 
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    
    gs = gameState()
    validMoves = gs.getValidMoves()
    moveMade = False
     

    #variabler till spelloopen
    loadImgs() #Gör bara en gång 
    run = True
    sqSelected = ()
    playerClicks = [] 
    while run: 
        for e in pygame.event.get():
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
                mouseLocation = pygame.mouse.get_pos()
                c = mouseLocation[0]//sqSize
                r = mouseLocation[1]//sqSize
                if sqSelected == (r,c):
                    sqSelected = ()
                    playerClicks = []
                else: 
                    sqSelected = (r,c)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: 
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
        
        
        if moveMade:
            validMoves = gs.getValidMoves()  
            moveMade = False  

        drawGs(screen,gs,sqSelected)
        clock.tick(maxFps)
        pygame.display.flip()

if __name__ == "__main__":
    main()