import pygame
import Config

# Função para exibir a tela de jogo (onde ficam a nave e inimigos)
def show_game_screen():
    bg = pygame.image.load('assets/media/bgSpace.png')
    bg = pygame.transform.scale(bg, (Config.Window.largura, Config.Window.altura))
    Config.Window.tela.blit(bg, (0, 0))

# Função para exibir o HUD (Heads Up Display) do jogo
def display_hud(player_lives, score):
    # Exibir o personagem, vidas e pontuação 
    piloto = pygame.image.load('assets/media/pilotFace.png') # Carregar a imagem do piloto
    piloto = pygame.transform.scale(piloto, (70, 70)) # Redimensionar a imagem do piloto
    vida = pygame.image.load('assets/media/Vida.png') # Carregar a imagem da vida(coxinha)
    vida = pygame.transform.scale(vida, (50, 50)) # Redimensionar a imagem da vida(coxinha)
    Config.Window.tela.blit(piloto, (8, 10)) # Exibir o piloto na tela
    for i in range(player_lives): # Exibir as vidas(coxinhas) do jogador
        Config.Window.tela.blit(vida, (50 + 20 * i, 10)) # Exibir as vidas(coxinhas) do jogador
    
    # Exibir a pontuação
    lives_text = Config.Font.font_small.render(f"Vidas: {player_lives}", True, (255, 255, 255)) # Renderizar o texto de vidas
    score_text = Config.Font.font_small.render(f"Pontuação:", True, (255, 255, 255)) # Renderizar o texto de pontuação
    score_points = Config.Font.font.render(f"{score}", True, (255, 255, 255)) # Renderizar a pontuação
    Config.Window.tela.blit(lives_text, (70, 50)) # Exibir o texto de vidas
    Config.Window.tela.blit(score_text, (Config.Window.largura - score_text.get_width() - 20, 30)) # Exibir o texto de pontuação
    Config.Window.tela.blit(score_points, (Config.Window.largura - score_text.get_width() - 10, 50)) # Exibir a pontuação

def show_start_screen():
    # Exibir tela inicial do jogo
    bg = pygame.image.load('assets/media/startBg.png')
    bg = pygame.transform.scale(bg, (Config.Window.largura, Config.Window.altura))
    Config.Window.tela.blit(bg,(0,0))
    start_text = Config.Font.font.render("Pressione ENTER para começar", True, (255, 255, 255))
    Config.Window.tela.blit(start_text, (Config.Window.largura // 2 - start_text.get_width() // 2, Config.Window.altura // 1.30))
    pygame.display.update()

def show_game_over_screen(score):
    # Exibir tela de game over e suas informações.
    bg = pygame.image.load('assets/media/gameoverBg.png')
    bg = pygame.transform.scale(bg, (Config.Window.largura, Config.Window.altura))
    Config.Window.tela.blit(bg,(0,0))
    score_text = Config.Font.font.render(f"Pontuação: {score}", True, (255, 255, 255))
    restart_text = Config.Font.font.render("Pressione R para jogar novamente", True, (255, 255, 255))
    Config.Window.tela.blit(score_text, (Config.Window.largura // 2 - score_text.get_width() // 2, Config.Window.altura // 2))
    Config.Window.tela.blit(restart_text, (Config.Window.largura // 2 - restart_text.get_width() // 2, Config.Window.altura // 1.5))
    pygame.display.update()

def show_victory_screen(score):
    # Exibir tela de vitória e suas informações.
    Config.Window.tela.fill((0, 0, 0))
    bg = pygame.image.load('assets/media/winBg.png')
    bg = pygame.transform.scale(bg, (Config.Window.largura, Config.Window.altura))
    Config.Window.tela.blit(bg,(0,0))
    score_text = Config.Font.font.render(f"Pontuação: {score}", True, (255, 255, 255))
    restart_text = Config.Font.font.render("Pressione R para jogar novamente", True, (255, 255, 255))
    Config.Window.tela.blit(score_text, (Config.Window.largura // 2 - score_text.get_width() // 2, Config.Window.altura // 2))
    Config.Window.tela.blit(restart_text, (Config.Window.largura // 2 - restart_text.get_width() // 2, Config.Window.altura // 1.5))
    pygame.display.update()
