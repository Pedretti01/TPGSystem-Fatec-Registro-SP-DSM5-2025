import pygame

# Inicializa o módulo de fontes (boa prática para evitar erros)
pygame.font.init()

# Caminho da fonte principal do projeto
FONT_PATH = "assets/font/Primitive.ttf"

# Fontes padronizadas para o jogo
FONT_BIG = pygame.font.Font(FONT_PATH, 36)
FONT_SMALL = pygame.font.Font(FONT_PATH, 24)

#Configurações de Janela
BASE_WIDTH = 1280
BASE_HEIGHT = 720

GROUND_LEVEL = 485

#Quadros por Segundos
FPS = 60

#Cores
BLACK_COLOR = [0,0,0]
WHITE_COLOR = [255,255,255]
BLUE_COLOR = [0,0,255]
LIGHT_SKY_BLUE_COLOR = [135, 206, 250]
GRAY_COLOR = [200, 200, 200]
YELLOW_COLOR = [255,200,0]
RED_COLOR = [255,0,0]
PURPLE_COLOR = [100,10,166]
ORANGE_COLOR = [255,136,0]
VENETIAN_RED_COLOR = [198,5,5]
TANGO_MANGA_COLOR = [227,119,5]
DEEP_MAGENTA_COLOR = [222,5,199]

