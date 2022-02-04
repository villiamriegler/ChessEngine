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




def drawGs(screen,gs):
    """
    Ritar all grafik för den nuvarande positionen på skärmen
    """
    drawSq(screen)
    drawPieces(screen, gs.board)

def drawSq(screen):
    colors = [pygame.Color("gray"),pygame.Color("dark gray")]
    for r in range(dim):
        for c in range(dim):
            color = (r+c)%2
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
    loadImgs() #Gör bara en gång 

    #variabler till spelloopen 
    run = True
    sqSelected = ()
    playerClicks = [] 
    while run: 
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                run = False

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    
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
                    print(move.getChessNot())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGs(screen, gs)
        clock.tick(maxFps)
        pygame.display.flip()

if __name__ == "__main__":
    main()