import imp
import pygame 
from chessEngine import *

width = height = 400
dim = 8 
sqSize = width / dim 
maxFps = 24 

images = {}

def loadImgs(): 
    pieces = ["wR","wN","wB","wQ","wK","wB","wN","wR","bR","bN","bB","bQ","bK","bB","bN","bR","wP","bP"]

    for p in pieces:
        images[p] = pygame.transform.scale(pygame.image.load("images/"+p+".png"),(sqSize,sqSize))

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))

    gs = gameState()
    print (gs.board)

main()