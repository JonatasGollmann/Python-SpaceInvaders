import pygame
from pygame.locals import *
import random

pygame.init()


# Configuração de tela
largura = 640       
altura = 680
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

# Configuração de jogador (Nave)
ship = pygame.image.load('assets/media/UnoNave.png')
ship = pygame.transform.scale(ship, (65, 65))
width = ship.get_width()
height = ship.get_height()
xShip = largura / 2 - width / 2
yShip = altura - height - 10
velShip = 4.5

# Configurações gerais
player_lives = 3
score = 0
game_state = "start"  # Estados: start, playing, game_over, victory

# Fonte para textos
font = pygame.font.SysFont(None, 26)
font_small = pygame.font.SysFont(None, 16)

# Lista de tiros
bullets = []
enemy_bullets = []

# Configuração de inimigos
enemy_image = pygame.image.load('assets/media/enemyCat.png')
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
enemy_width = enemy_image.get_width()
enemy_height = enemy_image.get_height()
enemy_vel = 1
enemy_direction = 1  # 1 para direita, -1 para esquerda


def start_music(music_dir):
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play(-1,fade_ms=5000)

# Classe Tiro
class Bullet:
    def __init__(self, x, y, vel, color):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = 5
        self.height = 10
        self.color = color

    def move(self):
        self.y += self.vel

    def draw(self):
        pygame.draw.rect(tela, self.color, (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y < 0 or self.y > altura  # Fora da tela

# Criar inimigos
# Criar inimigos
def create_enemies():
    enemies = []
    rows = 4
    cols = 6
    padding = 10
    for row in range(rows):
        for col in range(cols):
            x = col * (enemy_width + padding) + 50
            y = row * (enemy_height + padding) + 50
            enemies.append({
                "x": x,
                "y": y,
                "width": enemy_width,
                "height": enemy_height,
                "last_shot_time": 0  # Tempo do último tiro
            })
    return enemies


# Verificar colisão
def check_collision(obj1, obj2):
    return (
        obj1.x < obj2['x'] + obj2['width'] and
        obj1.x + obj1.width > obj2['x'] and
        obj1.y < obj2['y'] + obj2['height'] and
        obj1.y + obj1.height > obj2['y']
    )

# Funções de interface
def exibe_hud():
    piloto = pygame.image.load('assets/media/pilotFace.png')
    piloto = pygame.transform.scale(piloto, (70, 70))
    vida = pygame.image.load('assets/media/Vida.png')
    vida = pygame.transform.scale(vida, (50, 50))
    tela.blit(piloto, (8, 10))
    for i in range(player_lives):
        tela.blit(vida, (50 + 20 * i, 10))
    lives_text = font_small.render(f"Vidas: {player_lives}", True, (255, 255, 255))
    score_text = font_small.render(f"Pontuação:", True, (255, 255, 255))
    score_points = font.render(f"{score}", True, (255, 255, 255))
    tela.blit(lives_text, (70, 50))
    tela.blit(score_text, (largura - score_text.get_width() - 20, 30))
    tela.blit(score_points, (largura - score_text.get_width() - 10, 50))

def show_start_screen():
    bg = pygame.image.load('assets/media/startBg.png')
    bg = pygame.transform.scale(bg, (largura, altura))
    
    tela.blit(bg,(0,0))
    start_text = font.render("Pressione ENTER para começar", True, (255, 255, 255))
    tela.blit(start_text, (largura // 2 - start_text.get_width() // 2, altura // 1.30))
    pygame.display.update()

def show_game_over_screen():
    bg = pygame.image.load('assets/media/gameoverBg.png')
    bg = pygame.transform.scale(bg, (largura, altura))
    tela.blit(bg,(0,0))
    score_text = font.render(f"Pontuação: {score}", True, (255, 255, 255))
    restart_text = font.render("Pressione R para jogar novamente", True, (255, 255, 255))
    tela.blit(score_text, (largura // 2 - score_text.get_width() // 2, altura // 2))
    tela.blit(restart_text, (largura // 2 - restart_text.get_width() // 2, altura // 1.5))
    pygame.display.update()

def show_victory_screen():
    tela.fill((0, 0, 0))
    bg = pygame.image.load('assets/media/winBg.png')
    bg = pygame.transform.scale(bg, (largura, altura))
    tela.blit(bg,(0,0))
    score_text = font.render(f"Pontuação: {score}", True, (255, 255, 255))
    restart_text = font.render("Pressione R para jogar novamente", True, (255, 255, 255))
    tela.blit(score_text, (largura // 2 - score_text.get_width() // 2, altura // 2))
    tela.blit(restart_text, (largura // 2 - restart_text.get_width() // 2, altura // 1.5))
    pygame.display.update()

# Função principal do jogo
def main_game():
    global xShip, yShip, bullets, player_lives, score, game_state, enemy_direction

    # Variáveis de jogo
    enemies = create_enemies()
    bullets = []
    player_lives = 3
    score = 0
    last_shot_time = 0
    shot_cooldown = 500
    enemy_shoot_cooldown = 3000 

    # Loop do jogoz
    # Dentro do main_game():
    enemy_shoot_chance = 0.001 # Chance de um inimigo atacar em cada quadro

    while game_state == "playing":
        clock.tick(60)
        game_bg = pygame.image.load('assets/media/bg_space.png')
        game_bg = pygame.transform.scale(game_bg, (largura, altura))
        tela.blit(game_bg, (0, 0))
        
        if not pygame.mixer.music.get_busy():
            start_music('assets/sound/bgAnnaJulia.mp3')
        # Eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shot_time > shot_cooldown:
                        bullet = Bullet(xShip + width / 2 - 2.5, yShip, -10, (255, 0, 0))
                        shotSound = pygame.mixer.Sound('assets/sound/gunShip.mp3')
                        shotSound.play()
                        bullets.append(bullet)
                        last_shot_time = current_time

        # Movimentação da nave
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and xShip > 0:
            xShip -= velShip
        if keys[K_RIGHT] and xShip < largura - width:
            xShip += velShip

        # Atualizar inimigos
        # Atualizar inimigos
        move_down = False
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            enemy['x'] += enemy_vel * enemy_direction
            if enemy['x'] + enemy_width >= largura or enemy['x'] <= 0:
                move_down = True

            # Verificar cooldown do tiro
            if current_time - enemy['last_shot_time'] > enemy_shoot_cooldown:
                if random.random() < enemy_shoot_chance:
                    enemy_bullets.append(Bullet(enemy['x'] + enemy_width / 2, enemy['y'] + enemy_height, 5, (0, 255, 0)))
                    enemy_shotSound = pygame.mixer.Sound('assets/sound/gunEnemy.mp3')
                    enemy_shotSound.play()
                    enemy['last_shot_time'] = current_time  # Atualiza o tempo do último tiro

        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy['y'] += enemy_height // 2

        # Atualizar tiros do jogador
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            for enemy in enemies[:]:
                if check_collision(bullet, enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 50
                    break
            if bullet.off_screen():
                bullets.remove(bullet)
                score -= 10

        # Atualizar tiros dos inimigos
        for e_bullet in enemy_bullets[:]:
            e_bullet.move()
            e_bullet.draw()
            if (
                xShip < e_bullet.x < xShip + width and
                yShip < e_bullet.y < yShip + height
            ):
                damageSound = pygame.mixer.Sound('assets/sound/damageShip.mp3')
                damageSound.play()
                score -= 25
                player_lives -= 1
                enemy_bullets.remove(e_bullet)
            elif e_bullet.off_screen():
                enemy_bullets.remove(e_bullet)

        # Exibir HUD
        exibe_hud()

        # Desenhar nave e inimigos
        tela.blit(ship, (xShip, yShip))
        for enemy in enemies:
            tela.blit(enemy_image, (enemy['x'], enemy['y']))

        pygame.display.update()

    # Checar vitória ou derrota
        if not enemies:
            game_state = "victory"
            pygame.mixer.music.stop()
        if player_lives <= 0:
            game_state = "game_over"
            pygame.mixer.music.stop()


# Loop principal
while True:
    if game_state == "start":
        show_start_screen()
        if not pygame.mixer.music.get_busy():
            start_music('assets/sound/bgTemPerdido.mp3')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                game_state = "playing"
                pygame.mixer.music.stop()
                main_game()

    elif game_state == "game_over":
        show_game_over_screen()
        if not pygame.mixer.music.get_busy():
            start_music('assets/sound/bgVascou.mp3')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_r:
                pygame.mixer.music.stop()
                game_state = "playing"
                main_game()

    elif game_state == "victory":
        show_victory_screen()
        if not pygame.mixer.music.get_busy():
            start_music('assets/sound/bgCorVerAma.mp3')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_r:
                pygame.mixer.music.stop()
                game_state = "playing"
                main_game()
    