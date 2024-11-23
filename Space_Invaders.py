import pygame
from pygame.locals import *
import random
import Config
import Actions
from Pages import *
pygame.init()


# Configuração de tela e da janela
altura = Config.Window.altura
largura = Config.Window.largura
tela = Config.Window.tela
pygame.display.set_caption('Space Invaders')

# Configurações gerais
clock = pygame.time.Clock() # Relógio
game_state = "start"  # Estados do jogo: start, playing, game_over, victory
score = 0 # Pontuação


# Função principal do jogo
def main_game():
    bullets = [] # Lista de tiros
    enemy_bullets = [] # Lista de tiros dos inimigos
    global game_state, score
    ship = Actions.Ship() # Inicia a nave
    enemy = Actions.Enemy() # inicializa o inimigo
    xShip = ship.xShip # Posição x da nave
    yShip = ship.yShip # Posição y da nave
    enemies = Actions.create_enemies(enemy.height, enemy.width) # Cria os inimigos
    score = 0 # Pontuação inicial
    last_shot_time = 0 # Ultimo tempo onde foi dado o ultimo tiro.

    # Loop do jogo quando está em andamento
    while game_state == "playing":
        clock.tick(60) 
        show_game_screen() # Exibir tela de jogo (Background enquanto joga)
        
        if not pygame.mixer.music.get_busy(): # Se a música não estiver tocando toca a música de fundo
            Config.Music('assets/sound/bgAnnaJulia.mp3') # Música de fundo
        
        # Eventos do jogo, captura qualquer evento que ocorra.
        for event in pygame.event.get():
            #Filtragem de eventos
            # Se o evento for de fechar a janela, fecha o jogo
            if event.type == QUIT:
                pygame.quit()
                exit()
            # Se o evento for de apertar a tecla espaço, a nave atira.         
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    current_time = pygame.time.get_ticks() # Pega o tempo atual, para calcular o cooldown dos tiros.
                    # Verifica se o tempo atual - o tempo do ultimo tiro é maior que o cooldown do tiro.
                    if current_time - last_shot_time > ship.shot_cooldown:
                        # Cria um tiro na posição da nave
                        bullet = Actions.Bullet(xShip + ship.width / 2 - 2.5, yShip, -10, (255, 0, 0))
                        Config.Music.efects('assets/sound/gunShip.mp3') # Efeito sonoro do tiro
                        bullets.append(bullet) # Adiciona o tiro na lista de tiros
                        last_shot_time = current_time # Atualiza o tempo do ultimo tiro

        # Movimentação da nave do jogador, está fora do loop de eventos
        # para que a nave se mova mesmo se não houver eventos. (Ex: Tecla pressionada)
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and xShip > 0: # Se a tecla esquerda ou a for pressionada e a nave não estiver na borda esquerda
            xShip -= ship.velShip # Move a nave para a esquerda
        if (keys[K_RIGHT] or keys[K_d]) and xShip < largura - ship.width: # Se a tecla direita ou d for pressionada e a nave não estiver na borda direita
            xShip += ship.velShip # Move a nave para a direita

        # Atualizar inimigos, movimentação e tiros dos inimigos
        move_down = False # Variável para verificar se os inimigos devem se mover para baixo
        current_time = pygame.time.get_ticks() # Pega o tempo atual
        for e in enemies: 
            e['x'] += enemy.velEnemy * enemy.directionEnemy # Movimenta os inimigos para a direção (1 para direita e -1 para esquerda)
            if e['x'] + enemy.width >= largura or e['x'] <= 0: # Se os inimigos chegarem na borda da tela inverte a direção e move para baixo
                move_down = True

            # Verificar cooldown do tiro dos inimigos
            if current_time - e['last_shot_time'] > enemy.enemy_shoot_cooldown: # Verifica se o tempo atual - o tempo do ultimo tiro é maior que o cooldown do tiro.
                if random.random() < enemy.enemy_shoot_chance: # Se um número aleatório for menor que a chance de atirar
                    enemy_bullets.append(Actions.Bullet(e['x'] + enemy.width / 2, e['y'] + enemy.height, 5, (0, 255, 0))) # Cria um tiro do inimigo
                    Config.Music.efects('assets/sound/gunEnemy.mp3') # Efeito sonoro do tiro
                    e['last_shot_time'] = current_time  # Atualiza o tempo do último tiro

        if move_down: # Se os inimigos devem se mover para baixo (chegaram na borda da tela) ele inverte o lado para qual estavam se movimentando
            enemy.directionEnemy *= -1
            for e in enemies:
                e['y'] += enemy.height // 2

        # Atualizar tiros do jogador e verificar colisões
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            for e in enemies[:]:
                # Verifica se houve colisão entre o tiro e o inimigo
                if Actions.check_collision(bullet, e):
                    enemies.remove(e) # Remove o inimigo
                    bullets.remove(bullet) # Remove o tiro
                    score += 50 # Adiciona 50 pontos a pontuação
                    break
            if bullet.off_screen(): # Se o tiro sair da tela, remove o tiro e diminui 10 pontos da pontuação
                bullets.remove(bullet)
                score -= 10

        # Atualizar tiros dos inimigos
        for e_bullet in enemy_bullets[:]: # Para cada tiro dos inimigos, atualiza a posição e verifica colisões.
            e_bullet.move()
            e_bullet.draw()
            if (
                xShip < e_bullet.x < xShip + ship.width and
                yShip < e_bullet.y < yShip + ship.height
            ): # Verifica se houve colisão entre o tiro do inimigo e a nave e executa som de dano e remove o tiro.
                Config.Music.efects('assets/sound/damageShip.mp3')
                
                score -= 25 # Diminui 25 pontos da pontuação
                ship.lives -= 1 # Diminui uma vida da nave
                enemy_bullets.remove(e_bullet) # Remove o tiro
            elif e_bullet.off_screen(): # Se o tiro sair da tela, remove o tiro
                enemy_bullets.remove(e_bullet) # Remove o tiro

        # Exibir HUD
        display_hud(player_lives=ship.lives, score=score)

        # Desenhar nave e inimigos
        tela.blit(ship.ship, (xShip, yShip)) # Desenha a nave na tela
        for e in enemies:
            tela.blit(enemy.enemy, (e['x'], e['y'])) # Desenha os inimigos na tela

        pygame.display.update() # Atualiza a tela do jogo a cada nova atualização de ações.

    # Checar vitória ou derrota
        if not enemies: 
            game_state = "victory" # Se não houver mais inimigos, o jogador venceu
            Config.Music.stop() # Para a música de fundo
        if ship.lives <= 0: # Se a nave não tiver mais vidas, o jogador perdeu
            game_state = "game_over" # Muda o estado do jogo para game_over
            Config.Music.stop() # Para a música de fundo


# Loop principal
while True:
    if game_state == "start": # Se o estado do jogo for start, exibe a tela inicial
        show_start_screen() # Exibe a tela inicial
        if not pygame.mixer.music.get_busy(): # Se a música não estiver tocando toca a música de fundo
            Config.Music('assets/sound/bgTemPerdido.mp3')
        for event in pygame.event.get(): # Eventos da tela inicial
            if event.type == QUIT: # Se o evento for de fechar a janela, fecha o jogo
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_RETURN: # Se o evento for de apertar a tecla enter, inicia o jogo
                game_state = "playing" # Muda o estado do jogo para playing
                Config.Music.stop() # Para a música de fundo da pagina inicial
                main_game()  # Inicia o jogo

    elif game_state == "game_over": # Se o estado do jogo for game_over, exibe a tela de game_over
        show_game_over_screen(score) # Exibe a tela de game_over
        if not pygame.mixer.music.get_busy(): # Se a música não estiver tocando toca a música de fundo
            Config.Music('assets/sound/bgVascou.mp3') # Música de fundo
        for event in pygame.event.get(): # Eventos da tela de game_over
            if event.type == QUIT: # Se o evento for de fechar a janela, fecha o jogo
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_r: # Se o evento for de apertar a tecla r, reinicia o jogo
                Config.Music.stop()
                game_state = "playing"
                main_game()

    elif game_state == "victory": # Se o estado do jogo for victory, exibe a tela de vitória
        show_victory_screen(score) # Exibe a tela de vitória
        if not pygame.mixer.music.get_busy(): # Se a música não estiver tocando toca a música de fundo
            Config.Music('assets/sound/bgCorVerAma.mp3')
        for event in pygame.event.get(): # Eventos da tela de vitória
            if event.type == QUIT: # Se o evento for de fechar a janela, fecha o jogo
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_r: # Se o evento for de apertar a tecla r, reinicia o jogo
                Config.Music.stop()
                game_state = "playing"
                main_game()
    