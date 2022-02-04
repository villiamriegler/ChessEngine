import pygame 
from chessEngine import *

#Skärm variabler 
width = height = 512
dim = 8 
sqSize = width / dim 
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
    colors = [pygame.Color("gray"),pygame.Color("black")]
    for r in range(dim):
        for c in range(dim):
            color = (r+c)%2
            pygame.draw.rect(screen, colors[color], pygame.Rect(c*sqSize,r*sqSize,sqSize,sqSize))

def drawPieces(screen,board):
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = gameState()
    loadImgs() #Gör bara en gång 
    run = True 
    while run: 
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                run = False
        drawGs(screen, gs)
        clock.tick(maxFps)
        pygame.display.flip()

if __name__ == "__main__":
    main()