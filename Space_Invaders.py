import pygame
from pygame.locals import *
from sys import exit
import random
import time
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
yEnemy = random.randint(50, 150)
xEnemy = random.randint(0, 720)
velEnemy = 20


def draw_bg():
    bg = pygame.image.load('assets/bg_space.png')
    bg = pygame.transform.scale(bg, (largura, altura))
    tela.blit(bg, (0, 0))

def showEnemy(x,y):
    enemy = pygame.image.load('assets/enemy.png')
    enemy = pygame.transform.scale(enemy, (25, 25))
    tela.blit(enemy, (x, y))


def showShip(x, y):
    tela.blit(ship, (x, y))

run = True
while run:

    clock.tick(60)
    draw_bg()
    showShip(xShip, yShip)
    showEnemy(xEnemy, yEnemy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and xShip > velShip:
        xShip -= velShip
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and xShip < 720 - width:
        xShip += velShip
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and yShip > velShip:
        yShip -= velShip
    if (keys[K_DOWN] or keys[pygame.K_s]) and yShip < 640 - height:
        yShip += velShip
    
    xEnemy += velEnemy
    time.sleep(0.75)
    if xEnemy >= largura - 25 or xEnemy <= 0:
        velEnemy = -velEnemy
        yEnemy += 25
        
    pygame.display.update()

pygame.quit()