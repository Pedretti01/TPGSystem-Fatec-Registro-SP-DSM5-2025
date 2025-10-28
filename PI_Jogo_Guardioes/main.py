import pygame, sys, traceback
from script.scenes import *       # suas cenas (Login, GameOver, etc.)
from script.setting import *      # BASE_WIDTH, BASE_HEIGHT, FPS...
from script.obj import *          # Player, etc.
from script.controller import Controller  # 🎮 Novo módulo de controle USB
from script.layer_anim import *


class Game:
    def __init__(self):
        # Inicializa os módulos principais do pygame
        pygame.init()
        pygame.mixer.init()

        # Define ícone e título da janela
        icon = pygame.image.load("assets/menu/Icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Guardiões de Pindorama")

        # Cria a janela principal (pode ser redimensionada)
        self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)

        # Cria a tela virtual para manter proporção fixa (ex: 1280x720)
        self.virtual_screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

        # Controla FPS"
        self.clock = pygame.time.Clock()

        # Controle de tela cheia
        self.fullscreen = False

        # Cena inicial do jogo (pode trocar para Title, Map, etc.)
        self.scene = Login()

        # 🎮 Inicializa o módulo de controle USB
        self.controller = Controller()

    def run(self):
        try:
            while True:
                # === LOOP PRINCIPAL DO JOGO ===
                for event in pygame.event.get():
                    # 🎮 Traduz comandos do joystick para eventos de teclado
                    controller_event = self.controller.process_event(event)
                    if controller_event:
                        # Se houve tradução, substitui o evento original pelo equivalente do teclado
                        event = controller_event

                    # Fecha o jogo na cruz vermelha da janela
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Atalho para alternar entre janela e tela cheia (F11)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                        if self.fullscreen:
                            self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
                            self.fullscreen = False
                        else:
                            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            self.fullscreen = True

                    # Repassa evento para a cena atual (teclado + joystick já unificados)
                    if self.scene:
                        self.scene.handle_events(event)

                # Atualiza a lógica da cena atual
                if self.scene:
                    self.scene.update()

                    # Limpa a tela virtual
                    self.virtual_screen.fill("black")

                    # Desenha a cena atual na tela virtual
                    self.scene.draw(self.virtual_screen)

                    # Troca de cena, se necessário
                    if self.scene.next and self.scene.next is not self.scene:
                        self.scene = self.scene.next

                # === ESCALONAMENTO DA TELA VIRTUAL PARA A JANELA ===
                current_width, current_height = self.display.get_size()
                scale = min(current_width / BASE_WIDTH, current_height / BASE_HEIGHT)
                new_w, new_h = int(BASE_WIDTH * scale), int(BASE_HEIGHT * scale)
                offset_x = (current_width - new_w) // 2
                offset_y = (current_height - new_h) // 2

                # Redimensiona e centraliza
                scaled = pygame.transform.scale(self.virtual_screen, (new_w, new_h))
                self.display.fill("black")
                self.display.blit(scaled, (offset_x, offset_y))

                # Atualiza a tela visível
                pygame.display.flip()

                # Limita FPS
                self.clock.tick(FPS)

        except Exception:
            print("\n[ERRO FATAL NO GAME LOOP]")
            traceback.print_exc()
            pygame.time.delay(2000)

        finally:
            pygame.quit()
            sys.exit()


# Executa o jogo
if __name__ == "__main__":
    game = Game()
    game.run()

