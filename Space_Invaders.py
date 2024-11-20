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
velEnemy = 35
lastMoveEnemy = 0
moveIntervalEnemy = 750

shootShipInterval = 500
lastShipShot = 0

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


# Lista de tiros
bullets = []

# Classe Tiro
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10  # Velocidade do tiro
        self.width = 5
        self.height = 5
    
    def move(self):
        self.y -= self.vel  # O tiro sobe
        
    def draw(self):
        pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Cor vermelha
    
    def off_screen(self):
        return self.y < 0  # Se o tiro sair da tela

def check_collision(bullet, enemy_x, enemy_y, enemy_width, enemy_height):
    if (bullet.x > enemy_x and bullet.x < enemy_x + enemy_width and
        bullet.y > enemy_y and bullet.y < enemy_y + enemy_height):
        return True
    return False


run = True
while run:

    clock.tick(60)
    draw_bg()
    showShip(xShip, yShip)
    showEnemy(xEnemy, yEnemy)
      # Movimento do inimigo e detecção de colisão
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        
        # Verificar colisão com o inimigo
        if check_collision(bullet, xEnemy, yEnemy, 25, 25):
            # Se houver colisão, reposiciona o inimigo e remove o tiro
            xEnemy = random.randint(0, 720)
            yEnemy = random.randint(50, 150)
            bullets.remove(bullet)  # Remove o tiro que atingiu o inimigo

        # Remover tiros fora da tela
        if bullet.off_screen():
            bullets.remove(bullet)



    currentTime = pygame.time.get_ticks()
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
    # Tiro
    if keys[pygame.K_SPACE] and currentTime - lastShipShot >= shootShipInterval:
        # Criar um novo tiro
        bullet = Bullet(xShip + width / 2 - 2.5, yShip)  # Lança o tiro a partir do meio da nave
        bullets.append(bullet)
        lastShipShot = currentTime

    if currentTime - lastMoveEnemy >= moveIntervalEnemy:
        xEnemy += velEnemy
    
        if xEnemy >= largura - 25 or xEnemy <= 0:
            velEnemy = -velEnemy
            yEnemy += 25
        
        lastMoveEnemy = currentTime
        
    pygame.display.update()

pygame.quit()