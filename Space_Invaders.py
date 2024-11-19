import pygame
from pygame.locals import *
from sys import exit

pygame.init()

##Configuração de tela
largura = 720
altura = 640
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

##Configuração de jogador(Nave)
ship = pygame.image.load('assets/SpaceShip.png')
ship = pygame.transform.scale(ship, (50, 50))
width = ship.get_width()
height = ship.get_height()
xShip = largura/2 - width/2
yShip = altura - height - 10
velShip = 10

bg = pygame.image.load('assets/bg_space.png')
bg = pygame.transform.scale(bg, (largura, altura))
def draw_bg():
    tela.blit(bg, (0, 0))
    

def showShip(x, y):
    tela.blit(ship, (x, y))

run = True
while run:

    clock.tick(60)
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and xShip > velShip:
        xShip -= velShip
    if keys[pygame.K_RIGHT] and xShip < 720 - width:
        xShip += velShip
    if keys[K_UP] and yShip > velShip:
        yShip -= velShip
    if keys[K_DOWN] and yShip < 640 - height:
        yShip += velShip
    
    print(xShip, yShip)
    showShip(xShip, yShip)
    pygame.display.update()

pygame.quit()