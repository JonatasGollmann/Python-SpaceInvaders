
import pygame
pygame.init()

# Configurações gerais de janela e tela
class Window:
    largura = 640       
    altura = 680
    tela = pygame.display.set_mode((largura, altura))
    
# Configurações de fonte
class Font:
    font = pygame.font.SysFont(None, 26) # Fonte padrão
    font_small = pygame.font.SysFont(None, 16) # Fonte pequena

# Configurações de música
class Music:
    def __init__(self, music_dir): # Inicializa a música
        self.music_dir = music_dir # Diretório da música
        pygame.mixer.init() # Inicializa o mixer
        pygame.mixer.music.load(self.music_dir) # Carrega a música
        pygame.mixer.music.set_volume(0.5) # Volume da música
        pygame.mixer.music.play(-1,fade_ms=5000) # Toca a música em loop
    def stop(): # Função para parar a música
        pygame.mixer.music.stop() 
    def efects(music_dir): # Efeitos sonoros (tiros e dano)
        pygame.mixer.Sound(music_dir).play().set_volume(0.25)