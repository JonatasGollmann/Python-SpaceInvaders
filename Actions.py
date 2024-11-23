import pygame, Config
pygame.init()

# Função para verificar colisão entre dois objetos
def check_collision(obj1, obj2): # Verifica se houve colisão entre dois objetos
    return (
        obj1.x < obj2['x'] + obj2['width'] and
        obj1.x + obj1.width > obj2['x'] and
        obj1.y < obj2['y'] + obj2['height'] and
        obj1.y + obj1.height > obj2['y']
    )

# Função para criar inimigos, recebe a largura e altura do inimigo, retorna uma lista de inimigos
def create_enemies(enemy_width, enemy_height):
    enemies = []
    rows = 4 # Número de linhas de inimigos
    cols = 6 # Número de colunas de inimigos
    padding = 10 # Espaçamento entre os inimigos
    for row in range(rows):
        for col in range(cols):
            x = col * (enemy_width + padding) + 50
            y = row * (enemy_height + padding) + 50
            enemies.append({
                "x": x,
                "y": y,
                "width": enemy_width,
                "height": enemy_height,
                "last_shot_time": 0
            })
    return enemies

# Classe para a nave do jogador com suas informaçoes.
class Ship:
    def __init__(self):
        # Carregar a imagem da nave e redimensionar
        self.ship = pygame.image.load('assets/media/UnoNave.png')
        self.ship = pygame.transform.scale(self.ship, (65, 65))
        # Informações da nave
        self.width = self.ship.get_width()
        self.height = self.ship.get_height()
        self.xShip = Config.Window.largura / 2 - self.width / 2
        self.yShip = Config.Window.altura - self.height - 10
        self.velShip = 4.5
        self.shot_cooldown = 500
        self.lives = 3

# Classe para os inimigos com suas informações.
class Enemy:
    def __init__(self):
        # Carregar a imagem do inimigo e redimensionar
        self.enemy = pygame.image.load('assets/media/enemyCat.png')
        self.enemy = pygame.transform.scale(self.enemy, (50, 50))
        # Informações do inimigo
        self.width = self.enemy.get_width()
        self.height = self.enemy.get_height()
        self.velEnemy = 1
        self.directionEnemy = 1
        self.enemy_shoot_cooldown = 5000
        self.enemy_shoot_chance = 0.001

# Classe para os tiros com suas informações.
class Bullet:
    def __init__(self, x, y, vel, color):
        # Informações do tiro
        self.x = x
        self.y = y
        self.vel = vel
        self.width = 5
        self.height = 10
        self.color = color
    # Função para mover o tiro
    def move(self):
        self.y += self.vel
    # Função para desenhar o tiro
    def draw(self):
        pygame.draw.rect(Config.Window.tela, self.color, (self.x, self.y, self.width, self.height))
    # Função para verificar se o tiro saiu da tela
    def off_screen(self):
        return self.y < 0 or self.y > Config.Window.altura  # Fora da tela
