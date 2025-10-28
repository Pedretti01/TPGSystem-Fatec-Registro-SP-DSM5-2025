import pygame, sys, json  # Importa as bibliotecas necessárias
import random
from script.obj import *  # Importa todas as classes do módulo obj
from script.setting import *  # Importa todas as configurações do módulo setting
from script.layer_anim import LayerStack, StaticLayer, FlipLayer # Importa todas as configurações do módulo setting layer_anim


# ====== PROGRESSO GLOBAL DO MUNDO ======
# Quem lê/escreve: Level_1_2 (ao concluir) e Map (ao exibir bloqueios/ícones)
WORLD_PROGRESS = {
    "areas_done": set()   # ex.: {"Level_1_2", "Level_1_1"}
}


# Criando Classes para estruturar o Jogo:
# Criando Cenas
class Fade:
    def __init__(self, color="black"):
        self.color = color
        self.alpha = 0
        self.enabled = False

    def update(self):
        if self.enabled:
            self.alpha = min(255, self.alpha + 5)

    def draw(self, display):
        if self.enabled and self.alpha > 0:
            W, H = display.get_size()
            #s = pygame.Surface((W, H), pygame.SRCALPHA)
            #s.fill((0, 0, 0, self.alpha))
            #display.blit(s, (0, 0))


class PauseInventoryOverlay:
    """
    Overlay de pausa/inventário que desenha por cima da cena.
    Opções:
      - Retomar
      - Escambo (Loja)
      - Menu Inicial
    """
    def __init__(self, parent_scene, font, small_font, on_resume, on_shop, on_main_menu):
        self.parent_scene = parent_scene
        self.font = font
        self.small_font = small_font
        self.on_resume = on_resume
        self.on_shop = on_shop
        self.on_main_menu = on_main_menu

        self.options = ["Retomar", "Escambo (Loja)", "Menu Inicial"]
        self.selected = 0

        # Visual
        self.bg_alpha = 180  # opacidade do fundo escuro
        W, H = self.parent_scene.display.get_size()
        self.panel_width = int(W * 0.6)
        self.panel_height = int(H * 0.65)

        self.title_text = "Inventário & Pausa"
        # Tenta usar a mesma fonte com tamanho menor; se falhar, usa default.
        try:
            # Se a cena usou um caminho de fonte custom, reaproveite:
            self.small_font = pygame.font.Font(self.font.name, 24)  # type: ignore
        except Exception:
            self.small_font = pygame.font.Font(None, 24)

        # Integração com inventário real (substitua por player.inventory se tiver)
        self.inventory_items = self._read_inventory()

    def _read_inventory(self):
        # Placeholder: substitua pelo seu inventário real
        return [
            {"nome": "Poção de Cura", "qtd": 2},
            {"nome": "Cogumelo de Energia", "qtd": 1},
            {"nome": "Flecha de Taquara", "qtd": 18},
            {"nome": "Moedas", "qtd": 37},
        ]

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
                self.parent_scene.sound_click.play()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
                self.parent_scene.sound_click.play()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate_selected()
            elif event.key == pygame.K_ESCAPE:
                self.on_resume()
                

    def _activate_selected(self):
        option = self.options[self.selected]
        if option == "Retomar":
            self.on_resume()
        elif option == "Escambo (Loja)":
            self.on_shop()
        elif option == "Menu Inicial":
            self.on_main_menu()

    def update(self):
        # espaço para animações futuras
        pass

    def draw(self, display):
        W, H = display.get_size()

        # Fundo escurecido semi-transparente
        dim = pygame.Surface((W, H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, self.bg_alpha))
        display.blit(dim, (0, 0))

        # Painel central
        panel_rect = pygame.Rect(0, 0, self.panel_width, self.panel_height)
        panel_rect.center = (W // 2, H // 2)
        pygame.draw.rect(display, (30, 30, 30), panel_rect, border_radius=16)
        pygame.draw.rect(display, (200, 200, 200), panel_rect, width=2, border_radius=16)

        # Título
        title_surf = self.font.render(self.title_text, True, (240, 240, 240))
        title_rect = title_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 50))
        display.blit(title_surf, title_rect)

        # Colunas: à esquerda inventário, à direita opções
        padding = 28
        col_gap = 24

        left_rect = pygame.Rect(
            panel_rect.left + padding,
            title_rect.bottom + 20,
            int(self.panel_width * 0.55),
            panel_rect.bottom - (title_rect.bottom + 20) - padding
        )
        right_rect = pygame.Rect(
            left_rect.right + col_gap,
            left_rect.top,
            panel_rect.right - padding - (left_rect.right + col_gap),
            left_rect.height
        )

        # Inventário (lista simples)
        inv_title = self.small_font.render("Inventário", True, (210, 210, 210))
        display.blit(inv_title, (left_rect.x, left_rect.y))
        y = left_rect.y + 30
        for item in self.inventory_items:
            line = f"- {item['nome']} x{item['qtd']}"
            line_surf = self.small_font.render(line, True, (230, 230, 230))
            display.blit(line_surf, (left_rect.x + 8, y))
            y += 26

        # Opções
        opt_title = self.small_font.render("Opções", True, (210, 210, 210))
        display.blit(opt_title, (right_rect.x, right_rect.y))
        y = right_rect.y + 36
        for idx, opt in enumerate(self.options):
            selected = (idx == self.selected)
            color = (255, 255, 255) if selected else (200, 200, 200)
            opt_surf = self.font.render(opt, True, color)
            display.blit(opt_surf, (right_rect.x + 8, y))

            if selected:
                arrow = self.font.render("▶", True, color)
                display.blit(arrow, (right_rect.x - 36, y))
            y += 48


class Scene:
    """Classe base para todas as cenas do jogo."""
    
    def __init__(self, font_path="assets/font/Primitive.ttf", font_size=36):
        pygame.init()
        
        self.next = self                         # cena seguinte
        self.display = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        
        self.fade = Fade("black")                # efeito de fade
        self.sound_click = pygame.mixer.Sound("assets/sounds/click.ogg")
        self.sound_click.set_volume(0.25)
        
        self.option_data = self.load_file("teste.json")
        self.font = pygame.font.Font(font_path, font_size)

        # Controle de pausa/overlay
        self.paused = False
        self.overlay = None

    # ====== MENU DE PAUSA / INVENTÁRIO ======
    def open_pause_menu(self):
        """Cria e exibe o overlay de pausa/inventário com robustez."""
        try:
            if self.overlay is not None:
                return

            # garante um display válido
            if not self.display:
                self.display = pygame.display.get_surface()

            def on_resume():
                self.sound_click.play()
                self.overlay = None
                self.paused = False
                vol = self.option_data.get("music_set_volume")
                if vol is not None and pygame.mixer.get_init():
                    pygame.mixer.music.set_volume(vol)

            def on_shop():
                self.sound_click.play()
                self.change_scene(EscamboScene())

            def on_main_menu():
                self.sound_click.play()
                self.change_scene(Title())

            # cria o overlay com fallback seguro de fonte
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=on_resume,
                on_shop=on_shop,
                on_main_menu=on_main_menu
            )
            self.paused = True

            vol = self.option_data.get("music_set_volume")
            if vol is not None and pygame.mixer.get_init():
                pygame.mixer.music.set_volume(vol * 0.4)
        except Exception:
            import traceback; traceback.print_exc()
            # se der algo errado, não derrube o jogo: apenas desfaz o pause
            self.overlay = None
            self.paused = False

    def start_music(self):
        """Inicia música com checagens seguras."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            vol = self.option_data.get("music_set_volume", 0)
            pygame.mixer.music.load("assets/sounds/music1.mp3")
            if vol:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(vol)
        except Exception:
            import traceback; traceback.print_exc()

    # ====== EVENTOS ======
    def handle_events(self, event):
        # se overlay ativo → ele consome os eventos e pronto
        if self.overlay:
            self.overlay.handle_events(event)
            return

        # abre com ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_pause_menu()
            return
        # Subclasses tratam o resto

    # ====== DESENHO ======
    def draw(self, display):
        """Desenha sprites, fade e overlay."""
        self.all_sprites.draw(display)
        self.fade.draw(display)

        if self.overlay:
            self.overlay.draw(display)

    # ====== UPDATE ======
    def update(self):
        """Atualiza sprites, fade ou overlay."""
        if not self.paused:
            self.all_sprites.update()
            self.fade.update()
        else:
            if self.overlay:
                self.overlay.update()

    # ====== TROCA DE CENA ======
    def change_scene(self, next_scene):
        self.next = next_scene

    # ====== SALVAR / CARREGAR ======
    def save_file(self, arquivo, dados):
        with open(arquivo, "w") as dados_do_arquivo:
            json.dump(dados, dados_do_arquivo)
            print("OK")

    def load_file(self, arquivo):
        with open(arquivo, "r") as dados_do_arquivo:
            dados = json.load(dados_do_arquivo)
        return dados


# ====== CENAS DE PLACEHOLDER ======
class EscamboScene(Scene):
    def draw(self, display):
        super().draw(display)
        txt = self.font.render("ESCAMBO / LOJA (placeholder)", True, (255, 255, 0))
        display.blit(txt, (50, 50))


class MenuInicialScene(Scene):
    def draw(self, display):
        super().draw(display)
        txt = self.font.render("MENU INICIAL (placeholder)", True, (255, 255, 0))
        display.blit(txt, (50, 50))
    

    
# Criando Tela de Login de Usuário
class Login(Scene):
    """Classe para a tela de Login."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Carregando imagens de fundo e botões
        self.background = Obj("assets/login/background.png", [0, 0], [self.all_sprites])
        self.form_body = Obj("assets/login/FormBody.png", [428, 55], [self.all_sprites])
        self.login_button = Obj("assets/login/Button.png", [541, 460], [self.all_sprites])  # Botão de Login
                
        # Configuração de fontes
        self.title_font = pygame.font.Font(None, 36)  # Fonte para o título da tela
        self.label_font = pygame.font.Font(None, 24)  # Fonte para as labels de texto
        self.font = pygame.font.Font(None, 24)  # Fonte para campos de entrada
                
        # Campos de entrada
        self.RA_rect = pygame.Rect(470, 235, 340, 40)  # Campo de RA
        self.password_rect = pygame.Rect(470, 337, 340, 40)  # Campo de Senha
        self.active_field = None  # Para controlar qual campo está ativo
        self.login_button_rect = self.login_button.rect  # Retângulo do botão de login
        self.active_field = "RA"  # Inicia com o campo RA como ativo
        self.RA_text = ""
        self.password_text = ""
        
        # Cores para campos de entrada
        self.color_active = pygame.Color('dodgerblue')
        self.color_inactive = pygame.Color('gray')
        
        # Dados de login simulados (pode ser integrado com um banco de dados)
        #self.correct_login = "RA123456"
        #self.correct_password = "123"
    
    def validate_login(self):
        """Valida se o RA e Senha correspondem aos dados cadastrados."""
        return self.RA_text == self.correct_login and self.password_text == self.correct_password
    
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Apenas redireciona para a próxima tela ao pressionar Enter
                self.change_scene(Title())  # Redireciona para a próxima tela (Título)
        
        
        #Código Desativado para acesso sem Login e Senha
        #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_TAB:  # Quando TAB é pressionado, alterna o campo
                #if self.active_field == "RA":
                    #self.active_field = "Senha"  # Muda para o campo de Senha
                #elif self.active_field == "Senha":
                    #self.active_field = "Login"  # Muda para o botão de login
                #elif self.active_field == "Login":
                    #self.active_field = "RA"  # Muda de volta para o campo RA
            #elif self.active_field == "RA":
                #if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Salta para o campo de senha
                    #self.active_field = "Senha"
                #elif event.key == pygame.K_BACKSPACE:
                    #self.RA_text = self.RA_text[:-1]
                #else:
                    #self.RA_text += event.unicode
            #elif self.active_field == "Senha":
                #if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: # Verifica o login ao pressionar Enter
                    #if self.validate_login():
                        #self.change_scene(Title())  # Redireciona para a tela de título
                    #else:
                        #print("RA ou Senha Incorretos!")  # Mensagem de erro
                #elif event.key == pygame.K_BACKSPACE:
                    #self.password_text = self.password_text[:-1]
                #else:
                    #self.password_text += event.unicode
            #elif self.active_field == "Login":  # Se o foco estiver no botão de login
                #if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Verifica o login ao pressionar Enter
                    #if self.validate_login():
                        #self.change_scene(Title())  # Redireciona para a tela de título
                    #else:
                        #print("RA ou Senha Incorretos!")  # Mensagem de erro
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
        # Opcional: se você quiser permitir o clique no botão para avançar
            if self.login_button.rect.collidepoint(event.pos):
                self.change_scene(Title())  # Redireciona para a próxima tela (Título)
            
        
        #Código Desativado para acesso sem Login e Senha
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se o clique foi em algum dos campos de texto
            #if self.RA_rect.collidepoint(event.pos):
                #self.active_field = "RA"
            #elif self.password_rect.collidepoint(event.pos):
                #self.active_field = "Senha"
            #elif self.login_button_rect.collidepoint(event.pos):
                #self.active_field = "Login"
            #else:
                #self.active_field = None
            
            # Verifica clique no botão de login
            #if self.login_button.rect.collidepoint(event.pos):
                #if self.validate_login():
                    #self.change_scene(Title())  # Redireciona para a tela de título
                #else:
                    #print("RA ou Senha Incorretos!")  # Mensagem de erro
        
        return super().handle_events(event)
        
    def draw(self, surface):
        """Renderiza a tela de login."""
        surface.fill((0, 0, 0))  # Limpa a tela com uma cor de fundo

        # Desenha todos os sprites (background e botões)
        self.all_sprites.draw(surface)

        # Título da tela
        title_surface = self.title_font.render("Venha para a Aventura!", True, pygame.Color(BLACK_COLOR))
        title_rect = title_surface.get_rect(center=(surface.get_width() // 2, 120))  # Centraliza no eixo X e ajusta o eixo Y
        surface.blit(title_surface, title_rect.topleft)  # Usa o canto superior esquerdo do retângulo

        # Labels para os campos de entrada
        RA_label_surface = self.label_font.render("Digite seu RA:", True, pygame.Color(BLACK_COLOR))
        RA_label_rect = RA_label_surface.get_rect(topleft=(470, 209))  # Define posição inicial do texto RA
        surface.blit(RA_label_surface, RA_label_rect.topleft)

        password_label_surface = self.label_font.render("Digite sua Senha:", True, pygame.Color(BLACK_COLOR))
        password_label_rect = password_label_surface.get_rect(topleft=(470, 310))  # Define posição inicial do texto Senha
        surface.blit(password_label_surface, password_label_rect.topleft)

        # Desenha campos de texto
        RA_color = self.color_active if self.active_field == "RA" else self.color_inactive
        password_color = self.color_active if self.active_field == "Senha" else self.color_inactive

        pygame.draw.rect(surface, RA_color, self.RA_rect, 2)  # Contorno do campo RA
        pygame.draw.rect(surface, password_color, self.password_rect, 2)  # Contorno do campo Senha

        # Renderiza o texto digitado
        RA_surface = self.font.render(self.RA_text, True, pygame.Color(BLACK_COLOR))
        password_surface = self.font.render("*" * len(self.password_text), True, pygame.Color(BLACK_COLOR))  # Oculta senha com asteriscos

        surface.blit(RA_surface, (self.RA_rect.x + 5, self.RA_rect.y + 5))
        surface.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))
        
        # Destacar o botão de login quando estiver focado
        if self.active_field == "Login":
            pygame.draw.rect(surface, self.color_active, self.login_button_rect, 2)
        
    def update(self):
        """Atualiza a lógica da tela."""
        self.all_sprites.update()
        
# Criando Tela Inicial do Jogo
class Title(Scene):
    """Classe para a tela inicial do jogo."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Criação de objetos de fundo e outros elementos da tela
        self.bg = Obj("assets/menu/Fundo.png", [0, 0], [self.all_sprites], size=(1400, 850))
        self.bg_mold = Obj("assets/menu/Moldura_V2.png", [0, 0], [self.all_sprites])
        self.title = Obj("assets/menu/Titulo.png", [535, 50], [self.all_sprites], size=(700, 285))
        self.char1 = Obj("assets/menu/Indigena.png", [185, -10], [self.all_sprites], size=(450, 770))
        self.char2 = Obj("assets/menu/Bandeirantes.png", [12, 155], [self.all_sprites], size=(320, 575))
        self.char3 = Obj("assets/menu/Africano.png", [-240, 280], [self.all_sprites], size=(825, 650))
        self.star_text = Obj("assets/menu/Jogar.png", [822, 385], [self.all_sprites], size=(225, 80))
        self.options_text = Obj("assets/menu/Opcoes.png", [822, 485], [self.all_sprites], size=(275, 80))
        self.exit_text = Obj("assets/menu/Sair.png", [822, 585], [self.all_sprites], size=(175, 75))
        self.indicator = Obj("assets/menu/Cursor.png", [695, 385], [self.all_sprites], size=(110, 70))  # Cursor
        self.indicator_dir = 1  # Direção do movimento do cursor
        self.indicator_choose = 0  # Opção atualmente selecionada
        
        # Variáveis de movimento do BG
        self.bg_pos = [0, 0]  # Posição inicial do fundo
        self.bg_target = (-120, 0)  # Primeira posição alvo
        self.bg_vel = 1  # Velocidade de movimento do fundo

        # Pré-carregar a Música na memória e a opção de Tela Salva
        self.start_music()  # Inicia a música
        self.start_screen()  # Configura a tela inicial
        
    def start_screen(self):    
        """Configura a tela inicial com base nas opções salvas."""
        if self.option_data["display_text_values"] == "Fullscreen" and self.option_data["start"] == "on":
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Muda para tela cheia
            self.option_data["start"] = "off"  # Atualiza o estado
            self.save_file("teste.json", self.option_data)  # Salva as opções

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela inicial."""
        # Verifica se o evento recebido é uma tecla pressionada
        if event.type == pygame.KEYDOWN:
            # Enter (principal) ou Enter do keypad
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.indicator_set_option(event)
            # setas / WASD
            if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_UP, pygame.K_w):
                self.indicator_position(event)
        return super().handle_events(event)  # deixa o ESC subir para Scene

    def indicator_set_option(self, event):
        """Define a opção selecionada com base na tecla pressionada."""
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 0:
            self.change_scene(Control())  # Muda para a cena de seleção de personagem
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 1:
            self.change_scene(Option())  # Muda para a cena de opções
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 2:
            self.option_data["start"] = "on"  # Atualiza o estado
            self.save_file("teste.json", self.option_data)  # Salva os dados
            pygame.quit()  # Encerra o Pygame
            sys.exit()  # Sai do programa

    def indicator_position(self, event):
        """Atualiza a posição do indicador com base nas teclas pressionadas."""
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose <= 1:
                self.indicator_choose += 1  # Move para a próxima opção
                if self.indicator_choose == 0:
                    self.indicator.rect.y = 384  # Atualiza a posição do cursor
                elif self.indicator_choose == 1:
                    self.indicator.rect.y = 484
                elif self.indicator_choose == 2:
                    self.indicator.rect.y = 584
                        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose > 0:
                self.indicator_choose -= 1  # Move para a opção anterior
                if self.indicator_choose == 0:
                    self.indicator.rect.y = 384
                elif self.indicator_choose == 1:
                    self.indicator.rect.y = 484
                elif self.indicator_choose == 2:
                    self.indicator.rect.y = 584
     
    # Função auxiliar para mover o fundo até o alvo lentamente
    def move_towards_target(self, current, target, vel):
        """Move a posição atual em direção à posição alvo com a velocidade especificada."""
        if current < target:
            return min(current + vel, target)  # Move para frente até alcançar o alvo
        elif current > target:
            return max(current - vel, target)  # Move para trás até alcançar o alvo
        return current  # Retorna a posição atual se já estiver no alvo
            
    # Animando Cursor                            
    def update(self):
        """Atualiza a animação do cursor e o fundo."""
        self.indicator_animation()  # Atualiza a animação do cursor
    
        # Atualiza a animação do fundo
        return self.bg_animation()
    
    def bg_animation(self):
        """Movimenta o fundo de acordo com a lógica definida."""
        x, y = self.bg_pos  # Posições atuais do fundo
        
        # Movimentação do fundo entre as posições definidas
        if self.bg_target == (-120, 0):  # Movimento para a esquerda até x = -120
            x = self.move_towards_target(x, -120, self.bg_vel)
            if x == -120:
                self.bg_target = (-120, -130)  # Agora move para cima até y = -130
        
        elif self.bg_target == (-120, -130):  # Movimento para cima até y = -130
            y = self.move_towards_target(y, -130, self.bg_vel)
            if y == -130:
                self.bg_target = (0, -130)  # Agora move para a direita até x = 0
        
        elif self.bg_target == (0, -130):  # Movimento para a direita até x = 0
            x = self.move_towards_target(x, 0, self.bg_vel)
            if x == 0:
                self.bg_target = (0, 0)  # Agora move para baixo até y = 0
        
        elif self.bg_target == (0, 0):  # Movimento para baixo até y = 0
            y = self.move_towards_target(y, 0, self.bg_vel)
            if y == 0:
                self.bg_target = (-120, 0)  # Volta a mover para a esquerda, reiniciando o ciclo

        self.bg_pos = [x, y]  # Atualiza a posição do fundo
        self.bg.rect.topleft = self.bg_pos  # Define a nova posição do fundo
                
        return super().update()  # Chama o método update da classe pai

    def indicator_animation(self):
        """Anima o movimento do cursor."""
        self.indicator.rect.x += self.indicator_dir  # Move o cursor
        if self.indicator.rect.x > 705:  # Verifica os limites da animação
            self.indicator_dir *= -1  # Inverte a direção
        elif self.indicator.rect.x < 685:  # Verifica os limites da animação
            self.indicator_dir *= -1  # Inverte a direção

# Criando Tela de Opções
class Option(Scene):
    """Classe para a tela de opções."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
            
        # Criação de objetos de fundo e outros elementos da tela
        self.bg = Obj("assets/menu/Fundo2.png", [0, 0], [self.all_sprites], size=(1280, 720))
        self.bg_mold = Obj("assets/menu/Moldura_V2.png", [0, 0], [self.all_sprites])
        self.title = Obj("assets/menu/Titulo.png", [50, 50], [self.all_sprites], size=(500, 210))
        self.text_options = Obj("assets/menu/Opcoes.png", [850, 65], [self.all_sprites], size=(350, 100))
 
        # Criação de textos para opções de som e tela
        self.sound_text = Text(100, "Som:", VENETIAN_RED_COLOR, [360, 320], [self.all_sprites])
        self.sound_option_text = Text(60, self.option_data["sound_text_values"], YELLOW_COLOR, [670, 360], [self.all_sprites])
        self.sound_text_values = ["Desligado", "Minimo", "Maximo"]  # Opções de som
        self.sound_text_choose = self.option_data["sound_text_choose"]  # Opção de som selecionada
                
        self.display_text = Text(100, "Tela:", VENETIAN_RED_COLOR, [360, 450], [self.all_sprites])
        self.display_option_text = Text(60, self.option_data["display_text_values"], YELLOW_COLOR, [670, 490], [self.all_sprites])
        self.display_text_values = ["Window", "Fullscreen"]  # Opções de tela
        self.display_text_choose = self.option_data["display_text_choose"]  # Opção de tela selecionada
        
        self.apply_text = Text(60, "Aplicar:", TANGO_MANGA_COLOR, [508, 580], [self.all_sprites])
        
        # Inicialização do cursor
        self.indicator = Obj("assets/menu/Cursor.png", [217, 350], [self.all_sprites], size=(110, 70))  # Imagem do cursor
        self.indicator_dir = 1  # Direção do movimento do cursor
        self.indicator_choose = 0  # Opção atualmente selecionada
        
    def indicator_set_option(self, event):
        """Define a opção selecionada com base na tecla pressionada."""
        # Alternar opções de som
        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 0:
            if self.sound_text_choose < 2:
                self.sound_text_choose += 1  # Move para a próxima opção
            else:
                self.sound_text_choose = 0  # Retorna para a primeira opção
                
            self.option_data["sound_text_choose"] = self.sound_text_choose
            self.option_data["sound_text_values"] = self.sound_text_values[self.sound_text_choose]
                        
            # Atualiza o texto da opção de som
            self.sound_option_text.update_text(self.sound_text_values[self.sound_text_choose])
            
            # Ajusta a música de acordo com a seleção
            if self.sound_text_choose == 0:
                pygame.mixer.music.stop()  # Para a música
                self.option_data["music_set_volume"] = 0
            elif self.sound_text_choose == 1:
                self.option_data["music_set_volume"] = 0.05
                pygame.mixer.music.play(-1)  # Toca a música em loop
                pygame.mixer.music.set_volume(self.option_data["music_set_volume"])  # Ajusta o volume
            elif self.sound_text_choose == 2:
                self.option_data["music_set_volume"] = 0.1
                pygame.mixer.music.set_volume(0.1)  # Ajusta o volume

        # Alternar opções de tela
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 1:
            if self.display_text_choose < 1:
                self.display_text_choose += 1  # Move para a próxima opção
            else:
                self.display_text_choose = 0  # Retorna para a primeira opção
                
            self.display_option_text.update_text(self.display_text_values[self.display_text_choose])  # Atualiza o texto da opção de tela
            
            self.option_data["display_text_choose"] = self.display_text_choose
            self.option_data["display_text_values"] = self.display_text_values[self.display_text_choose]
                       
            # Aplica as mudanças na tela
            if self.display_text_choose == 0:
                pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)  # Modo janela
            elif self.display_text_choose == 1:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Modo tela cheia
                
        elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.indicator_choose == 2:
            self.save_file("teste.json", self.option_data)  # Salva as opções
            self.change_scene(Title())  # Retorna para a tela inicial
    
    def indicator_position(self, event):
        """Atualiza a posição do indicador com base nas teclas pressionadas."""
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose <= 1:
                self.indicator_choose += 1  # Move para a próxima opção
                if self.indicator_choose == 0:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 350
                elif self.indicator_choose == 1:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 480
                elif self.indicator_choose == 2:
                    self.indicator.rect.x = 365
                    self.indicator.rect.y = 570
                        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.sound_click.play()  # Toca o som de clique
            if self.indicator_choose > 0:
                self.indicator_choose -= 1  # Move para a opção anterior
                if self.indicator_choose == 0:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 350
                elif self.indicator_choose == 1:
                    self.indicator.rect.x = 217
                    self.indicator.rect.y = 480
                elif self.indicator_choose == 2:
                    self.indicator.rect.x = 365
                    self.indicator.rect.y = 570
                    
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de opções."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_UP, pygame.K_w):
                self.indicator_position(event)
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.indicator_set_option(event)
        return super().handle_events(event)
    
    def indicator_animation(self):
        """Anima o movimento do cursor."""
        self.indicator.rect.x += self.indicator_dir  # Move o cursor
        if 207 <= self.indicator.rect.x <= 227:  # Verifica os limites da animação
            if self.indicator.rect.x >= 227 or self.indicator.rect.x <= 207:
                self.indicator_dir *= -1  # Inverte a direção
        elif 355 <= self.indicator.rect.x <= 375:  # Verifica os limites da animação
            if self.indicator.rect.x >= 375 or self.indicator.rect.x <= 355:
                self.indicator_dir *= -1  # Inverte a direção
            
    def update(self):
        """Atualiza a animação do cursor e a tela."""
        self.indicator_animation()  # Atualiza a animação do cursor
        return super().update()  # Chama o método update da classe pai
 
# Criando Tela de Controles
class Control(Scene):
    """Classe para a tela de Controle."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        self.img = Obj("assets/Control.png", [0, 0], [self.all_sprites])  # Carrega a imagem de Game Over
        
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de Game Over."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.change_scene(Char_Select())  # Muda para a tela inicial            
        return super().handle_events(event)
    
    def draw(self, surface):
        """Desenha a tela de Game Over."""
        self.img.draw(surface)
        
class Char_Select(Scene):
    """Classe para a tela de seleção de personagens."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Fundo e Moldura
        try:
            self.bg = Obj("assets/charSelect/Fundo2.png", [0, 0], [self.all_sprites])  # Fundo da seleção
            self.bg_mold = Obj("assets/charSelect/Moldura_V3.png", [0, 0], [self.all_sprites], size=(1280, 720))  # Moldura da tela
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo ou moldura: {e}")

        # Cursor
        self.cursor_pos = [0, 0]  # Posição inicial [linha, coluna]
        self.cursor = Obj("assets/charSelect/IndChar.png", [21, 14], [self.all_sprites], size=(192, 247)) # Imagem do cursor
        self.cursor_choose = 0 # Índice do personagem selecionado
        
        # (Opcional) Placa antiga — se quiser usar, descomente
        # self.plate = Obj("assets/charSelect/placa.png", [733, 353], [self.all_sprites], size=(500, 310))
        
        # Estrutura de dados para personagens (novo formato)
        self.characters = [
            # NOVO FORMATO (exemplo)
            {
                "image_selected": "assets/charSelect/IM_C.png",
                "position_img_sel": [48, 45],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/IM_PB.png",
                "position_img_unsel": [57, 57],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/IM_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/IM_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/IM_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/IF_C.png",
                "position_img_sel": [190, 45],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/IF_PB.png",
                "position_img_unsel": [199, 57],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/IF_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/IF_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/IF_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/EM_C.png",
                "position_img_sel": [48, 268],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/EM_PB.png",
                "position_img_unsel": [57, 280],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/EM_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/EM_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/EM_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/EF_C.png",
                "position_img_sel": [190, 268],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/EF_PB.png",
                "position_img_unsel": [199, 280],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/EF_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/EF_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/EF_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/AM_C.png",
                "position_img_sel": [48, 487],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/AM_PB.png",
                "position_img_unsel": [57, 499],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/AM_P.png",
                "position_pose": [203, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/AM_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/AM_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
            {
                "image_selected": "assets/charSelect/AF_C.png",
                "position_img_sel": [190, 487],
                "size_position_img_sel": (138, 193),

                "image_unselected": "assets/charSelect/AF_PB.png",
                "position_img_unsel": [199, 499],
                "size_position_img_unsel": (120, 169),

                "pose": "assets/charSelect/AF_P.png",
                "position_pose": [251, 102],
                "size_pose": (550, 550),

                "description": "assets/charSelect/AF_D.png",
                "position_desc": [660, 18],
                "size_desc": (600, 372),

                "status": "assets/charSelect/AF_S.png",
                "position_status": [694, 381],
                "size_status": (550, 300)
            },
        ]

        # Grupo separado só para as miniaturas (evita apagar fundo/moldura/cursor)
        self.thumb_sprites = pygame.sprite.Group()

        # Carregar a imagem do primeiro personagem ao iniciar
        self.load_character(self.cursor_choose)
        
        # Matriz de posições do cursor (mantive a navegação 2x3 que você já usa)
        self.cursor_positions = [
            [21, 14], [163, 14],
            [21, 235], [163, 235],
            [21, 455], [163, 455]
        ]

    # -------------------- Helpers de compatibilidade --------------------
    def _thumb_fields(self, character, selected):
        """Retorna (img_path, pos, size) para a miniatura, compatível com os dois formatos."""
        if selected:
            # novo formato
            path = character.get("image_selected")
            pos  = character.get("position_img_sel")
            size = character.get("size_position_img_sel")
            # fallback antigo
            if pos is None:
                pos = character.get("position")
            if size is None:
                size = character.get("size_selected")
        else:
            path = character.get("image_unselected")
            pos  = character.get("position_img_unsel")
            size = character.get("size_position_img_unsel")
            if pos is None:
                pos = character.get("position")
            if size is None:
                size = character.get("size_unselected")
        return path, pos, size

    def _pose_fields(self, character):
        """Retorna (img_path, pos, size) da pose, compatível com os dois formatos."""
        path = character.get("pose")
        pos  = character.get("position_pose", character.get("pose_position"))
        size = character.get("size_pose", character.get("pose_size"))
        return path, pos, size

    def _desc_fields(self, character):
        """Retorna (img_path, pos, size) da descrição/histórico, compatível com os dois formatos."""
        path = character.get("description", character.get("history"))
        # padrão antigo usava [740, 60] e (500, 290) no seu draw_history
        pos  = character.get("position_desc", [740, 60])
        size = character.get("size_desc", (500, 290))
        return path, pos, size

    def _status_fields(self, character):
        """Retorna (img_path, pos, size) do status/placa de status, compatível com os dois formatos."""
        path = character.get("status", character.get("status_image"))
        # no seu draw_status_image: [760,380], (450,240)
        pos  = character.get("position_status", [760, 380])
        size = character.get("size_status", (450, 240))
        return path, pos, size

    # -------------------- Carregar sprites de miniaturas --------------------
    def load_character(self, index):
        """Recria APENAS as miniaturas conforme o personagem selecionado, mantendo fundo/moldura/cursor."""
        # limpa somente as thumbs
        for spr in list(self.thumb_sprites):
            spr.kill()
        self.thumb_sprites.empty()

        # recria thumbs (selecionada e não selecionadas)
        for i, character in enumerate(self.characters):
            # Carregar a imagem destacada (selecionada) para o personagem ativo
            selected = (i == index)
            img_path, pos, size = self._thumb_fields(character, selected)
            if not img_path or not pos or not size:
                continue
            Obj(img_path, pos, [self.thumb_sprites], size=size)

    # -------------------- Eventos --------------------
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de seleção de personagens."""
        if event.type == pygame.KEYDOWN:
            # Verifica se a tecla Enter foi pressionada
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Salvar o personagem selecionado
                self.option_data["selected_character"] = self.cursor_choose
                self.save_file("teste.json", self.option_data)  # Salva os dados
                
                if self.cursor_choose == 0:  # Se o primeiro personagem for selecionado
                    self.change_scene(Map())  # Muda para a cena do mapa

            # Movimento do cursor para baixo
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.cursor_choose + 2 < len(self.cursor_positions):  # Permite mover até o último personagem
                    self.cursor_choose += 2  # Move para o próximo personagem na coluna
                self.cursor.rect.y = self.cursor_positions[self.cursor_choose][1]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição

            # Movimento do cursor para cima
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.cursor_choose - 2 >= 0:  # Permite mover para cima se não estiver na primeira linha
                    self.cursor_choose -= 2  # Move para o personagem anterior na coluna
                self.cursor.rect.y = self.cursor_positions[self.cursor_choose][1]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição

            # Movimento do cursor para a direita
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.cursor_choose % 2 == 0 and self.cursor_choose + 1 < len(self.cursor_positions):  # Limita à primeira coluna
                    self.cursor_choose += 1  # Move para a direita
                self.cursor.rect.x = self.cursor_positions[self.cursor_choose][0]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição

            # Movimento do cursor para a esquerda
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.cursor_choose % 2 == 1:  # Limita à segunda coluna
                    self.cursor_choose -= 1  # Move para a esquerda
                self.cursor.rect.x = self.cursor_positions[self.cursor_choose][0]  # Atualiza a posição do cursor
                self.load_character(self.cursor_choose)  # Carrega o personagem na nova posição
    
    # -------------------- Draw --------------------
    def draw(self, screen):
        """Desenha a cena de seleção de personagens na tela."""
        # 1) Fundo
        self.bg.draw(screen)

        # 2) Miniaturas
        self.thumb_sprites.draw(screen)

        # 3) Descrição
        current = self.characters[self.cursor_choose]
        desc_path, desc_pos, desc_size = self._desc_fields(current)
        if desc_path and desc_pos and desc_size:
            Obj(desc_path, desc_pos, [self.all_sprites], size=desc_size).draw(screen)

        # 4) Status
        status_path, status_pos, status_size = self._status_fields(current)
        if status_path and status_pos and status_size:
            Obj(status_path, status_pos, [self.all_sprites], size=status_size).draw(screen)

        # 5) Cursor
        self.cursor.draw(screen)

        # 6) Moldura
        self.bg_mold.draw(screen)

        # 7) **POSE POR ÚLTIMO** (fica acima de tudo)
        pose_path, pose_pos, pose_size = self._pose_fields(current)
        if pose_path and pose_pos and pose_size:
            Obj(pose_path, pose_pos, [self.all_sprites], size=pose_size).draw(screen)

        pygame.display.update()


# Criando Tela de Mapa
class Map(Scene):
    """Classe para a tela do mapa com desenho por layers e áreas travadas quando concluídas."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai
        
        # -----------------------------
        #  LAYERS ESTÁTICOS DO CENÁRIO
        # -----------------------------
        try:
            # (opcional/estético) mar ao fundo — está no all_sprites, mas não é parte da ordem principal
            self.mar = Obj("assets/mapSelect/Mar.jpg", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # 1) 00Papiro  (primeiro a ser desenhado)
            self.papiro = Obj("assets/mapSelect/00Papiro.png", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # 2) 02Mapa_NovaPindorama_Fundo (base do mapa)
            self.bgMap  = Obj("assets/mapSelect/02Mapa_NovaPindorama_Fundo.png", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # (extra) contorno do mapa – desenhado depois do layer dinâmico para ficar por cima, se você quiser
            self.contMap = Obj("assets/mapSelect/01Mapa_NovaPindorama_Contorno.png", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # Moldura (último de todos)
            self.bg_mold = Obj("assets/mapSelect/Moldura_V1.png", [0, 0], [self.all_sprites], size=(1280, 720))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo ou moldura: {e}")

        # -----------------------------
        #  ÁREAS / SELEÇÃO / PROGRESSO
        # -----------------------------
        self.areas = self.initialize_areas()  # lista com caminhos e posições
        self.completed_areas_status = [False] * len(self.areas)  # status de conclusão por índice

        # Cursor
        self.cursor = Obj("assets/mapSelect/Cursor.png", [1070, 100], [self.all_sprites], size=(30, 48))
        self.cursor_positions = [area["cursor_position"] for area in self.areas]

        # Índice selecionado (mantemos compatibilidade com seu código antigo)
        self.cursor_choose = 0
        self.current_index = self.cursor_choose

        # Overlay do Vilarejo Canaã COMPLETO (layer 3 quando concluído)
        # ⚠️ carregamos como Surface isolada para NÃO depender do all_sprites (que é limpo pelo load_area)
        try:
            self.overlay_vilarejo_complete = pygame.image.load(
                "assets/mapSelect/00Vilarejo_Canaa_Complete.png"
            ).convert_alpha()
            # se precisar de escala fixa:
            self.overlay_vilarejo_complete = pygame.transform.scale(self.overlay_vilarejo_complete, (1280, 720))
        except Exception as e:
            print("[Map] Falha ao carregar 00Vilarejo_Canaa_Complete.png:", e)
            self.overlay_vilarejo_complete = None

        # Aplica progresso global (trava concluídas e posiciona cursor)
        self.apply_world_progress()

        # Carrega a camada dinâmica da área selecionada inicialmente
        self.load_area(self.current_index)  # usa regra "selected vs completed" da própria área

        # 🔽 Menu de pausa (como no seu original)
        from script.setting import FONT_BIG, FONT_SMALL
        self.pause_menu = PauseInventoryOverlay(
            parent_scene=self,
            font=FONT_BIG,
            small_font=FONT_SMALL,
            on_resume=self.resume_game,
            on_shop=self.goto_shop,
            on_main_menu=self.goto_menu
        )

        self.next = None

    # -----------------------------------------------------
    #  DEFINIÇÃO DAS ÁREAS (ordem do seu array de seleção)
    # -----------------------------------------------------
    def initialize_areas(self):
        """Inicializa as áreas do mapa com suas respectivas informações."""
        return [
            {  # 0 - Vilarejo Canaã (Level_1_2) -> fica TRAVADO quando concluído
                "image_selected": "assets/mapSelect/00Vilarejo_Canaa.png",
                "area_completed": "assets/mapSelect/00Vilarejo_Canaa_Complete.png",
                "position": [0, 0],
                "cursor_position": (1070, 100)
            },
            {  # 1 - Vila da Enseada do Rio (próximo ponto)
                "image_selected": "assets/mapSelect/01Vila_Enseada_Rio.png",
                "area_completed": "assets/mapSelect/01Vila_Enseada_Rio_Complete.png",
                "position": [0, 0],
                "cursor_position": (500, 130)
            },
            {  # 2 - Povoado Cadastro
                "image_selected": "assets/mapSelect/02Povoado_Cadastro.png",
                "area_completed": "assets/mapSelect/02Povoado_Cadastro_Complete.png",
                "position": [0, 0],
                "cursor_position": (650, 240)
            },
            {  # 3 - Vilarejo Grandes Pássaros
                "image_selected": "assets/mapSelect/03Vilarejo_Grandes_Passaros.png",
                "area_completed": "assets/mapSelect/03Vilarejo_Grandes_Passaros_Complete.png",
                "position": [0, 0],
                "cursor_position": (760, 180)
            },
            {  # 4 - Vale Luz & Sombra
                "image_selected": "assets/mapSelect/04Vale_Luz_Sombra.png",
                "area_completed": "assets/mapSelect/04Vale_Luz_Sombra_Complete.png",
                "position": [0, 0],
                "cursor_position": (850, 370)
            },
            {  # 5 - Freguesia Rio Peixes
                "image_selected": "assets/mapSelect/05Freguesia_Rio_Peixes.png",
                "area_completed": "assets/mapSelect/05Freguesia_Rio_Peixes_Complete.png",
                "position": [0, 0],
                "cursor_position": (450, 310)
            },
            {  # 6 - Vilarejo Praia Pequena
                "image_selected": "assets/mapSelect/06Vilarejo_Praia_Pequena.png",
                "area_completed": "assets/mapSelect/06Vilarejo_Praia_Pequena_Complete.png",
                "position": [0, 0],
                "cursor_position": (350, 230)
            },
            {  # 7 - Vila Pássaro Vermelho
                "image_selected": "assets/mapSelect/07Vila_Passaro_Vermelho.png",
                "area_completed": "assets/mapSelect/07Vila_Passaro_Vermelho_Complete.png",
                "position": [0, 0],
                "cursor_position": (880, 200)
            },
            {  # 8 - Vilarinho Pedras Fluem
                "image_selected": "assets/mapSelect/08Vilarinho_Pedras_Fluem.png",
                "area_completed": "assets/mapSelect/08Vilarinho_Pedras_Fluem_Complete.png",
                "position": [0, 0],
                "cursor_position": (250, 100)
            },
            {  # 9 - Barragem Arco-Íris
                "image_selected": "assets/mapSelect/09Barragem_Arco_Iris.png",
                "area_completed": "assets/mapSelect/09Barragem_Arco_Iris_Complete.png",
                "position": [0, 0],
                "cursor_position": (600, 380)
            },
            {  # 10 - Vale Alecrins
                "image_selected": "assets/mapSelect/10Vale_Alecrins.png",
                "area_completed": "assets/mapSelect/10Vale_Alecrins_Complete.png",
                "position": [0, 0],
                "cursor_position": (170, 160)
            },
            {  # 11 - Bosque Cajas
                "image_selected": "assets/mapSelect/11Bosque_Cajas.png",
                "area_completed": "assets/mapSelect/11Bosque_Cajas_Complete.png",
                "position": [0, 0],
                "cursor_position": (960, 260)
            },
        ]

    # -----------------------------------------------------
    #  PROGRESSO GLOBAL → TRAVAR + POSICIONAR CURSOR
    # -----------------------------------------------------
    def apply_world_progress(self):
        """
        Lê WORLD_PROGRESS e marca áreas concluídas.
        Também posiciona o cursor na próxima área disponível.
        """
        done = WORLD_PROGRESS.get("areas_done", set())

        # Mapeie "id da fase" -> índice da área na tela de mapa
        # Aqui ligamos Level_1_2 ao índice 0 (Vilarejo Canaã)
        level_to_index = {
            "Level_1_2": 0,
        }

        # Marca como concluídas
        for level_id in done:
            idx = level_to_index.get(level_id)
            if idx is not None and 0 <= idx < len(self.completed_areas_status):
                self.completed_areas_status[idx] = True

        # Se Level_1_2 foi concluído, cursor vai para "Vila da Enseada do Rio" (índice 1)
        VILA_ENSEADA_IDX = 1
        if "Level_1_2" in done and 0 <= VILA_ENSEADA_IDX < len(self.areas):
            self.current_index = VILA_ENSEADA_IDX
        else:
            # fallback: se onde estamos já está concluído, pula para próxima desbloqueada
            if self.completed_areas_status[self.current_index]:
                self.current_index = self._next_unlocked_index(self.current_index, step=+1)

        # mantém compatibilidade com o restante do código
        self.cursor_choose = self.current_index
        self.update_cursor_position()

    def _next_unlocked_index(self, start, step=+1):
        """
        Retorna o próximo índice NÃO concluído a partir de 'start',
        caminhando em 'step' (+1 direita, -1 esquerda).
        Se TODAS estiverem concluídas, retorna o próprio start.
        """
        n = len(self.areas)
        i = start
        for _ in range(n):
            i = (i + step) % n
            if not self.completed_areas_status[i]:
                return i
        return start

    def _is_locked(self, idx: int) -> bool:
        """Travado = já concluído."""
        return bool(self.completed_areas_status[idx])

    # -----------------------------------------------------
    #  CARREGAR LAYER DINÂMICO DA ÁREA SELECIONADA
    # -----------------------------------------------------
    def load_area(self, index):
        """
        Carrega a IMAGEM da área selecionada (layer dinâmico por cima do fundo).
        OBS: mantém sua lógica de limpar e repor sprites da área;
        por isso o overlay de 'Vilarejo_Canaa_Complete' foi carregado como Surface separada.
        """
        # limpa somente sprites de ÁREA, preservando os estáticos já desenhados por draw()
        # (para manter seu comportamento original, deixamos como estava:)
        self.all_sprites.empty()

        area = self.areas[index]
        # Se a área está concluída, usamos a arte 'Complete' como layer dinâmico
        area_image_path = area["image_selected"] if not self.completed_areas_status[index] else area["area_completed"]
        Obj(area_image_path, area["position"], [self.all_sprites])

        # atualiza posição do cursor
        self.update_cursor_position()

    def mark_area_as_completed(self):
        """Marca a área atual como completada (caso precise em outra lógica)."""
        self.completed_areas_status[self.cursor_choose] = True

    # -----------------------------------------------------
    #  ENTRAR NA ÁREA SELECIONADA (somente se desbloqueada)
    # -----------------------------------------------------
    def _enter_current_area(self):
        """
        Troca para a cena correspondente ao índice atual.
        ⚠️ Só é chamado se NÃO estiver travada.
        """
        idx = self.current_index

        # Mapeie aqui: indice -> cena
        if idx == 0:
            # Vilarejo Canaã (Level_1_1) — normalmente travado após concluir
            self.change_scene(Level())
        elif idx == 1:
            # Vila da Enseada do Rio -> troque pela cena correta quando existir
            # self.change_scene(Level_X_Y())
            print("[Map] TODO: vincular cena da Vila da Enseada do Rio (idx=1)")
        else:
            print(f"[Map] TODO: vincular cena para índice {idx}")

    # -----------------------------------------------------
    #  EVENTOS: NAVEGAÇÃO + ENTRAR (pulando travadas)
    # -----------------------------------------------------
    def handle_events(self, event):
        # ✅ Delegue para Scene (abre pausa com ESC, etc.)
        super().handle_events(event)
        
        if self.overlay:
            return
        
        if event.type == pygame.KEYDOWN:
            # ➡️ Direita: pula áreas concluídas
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.current_index = self._next_unlocked_index(self.current_index, step=+1)
                self.cursor_choose = self.current_index
                self.load_area(self.current_index)

            # ⬅️ Esquerda: idem
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.current_index = self._next_unlocked_index(self.current_index, step=-1)
                self.cursor_choose = self.current_index
                self.load_area(self.current_index)

            # ✅ Confirmar entrada (somente se NÃO estiver travada)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e, pygame.K_SPACE):
                if not self._is_locked(self.current_index):
                    self._enter_current_area()
                else:
                    print("[Map] Área concluída/travada — não pode entrar.")

    # -----------------------------------------------------
    #  CURSOR
    # -----------------------------------------------------
    def update_cursor_position(self):
        """Atualiza a posição do cursor com base na área selecionada (índice atual)."""
        # mantém compatibilidade com self.cursor_choose
        self.cursor_choose = self.current_index
        cursor_x, cursor_y = self.cursor_positions[self.current_index]
        self.cursor.rect.topleft = (cursor_x, cursor_y)

    # (mantém compatibilidade; não é usada diretamente na nova confirmação)
    def confirm_selection(self):
        """Confirma a seleção da área atual (compatibilidade)."""
        if not self.completed_areas_status[self.cursor_choose]:
            selected_area = self.areas[self.cursor_choose]["image_selected"]
            print(f"Área selecionada: {selected_area}")
            self.next = Level(selected_area)  # legado; não usado com _enter_current_area()
        else:
            print("Esta área já foi completada.")

    # -----------------------------------------------------
    #  DESENHO POR LAYERS — ORDEM EXATA
    # -----------------------------------------------------
    def draw(self, screen):
        """Desenha a tela do mapa na ordem: 00Papiro → 02Fundo → (overlay concluído) → área selecionada → contorno → moldura."""
        # 1) (opcional) mar — fica atrás do papiro na sua composição
        self.mar.draw(screen)

        # 2) 00Papiro
        self.papiro.draw(screen)

        # 3) 02Mapa_NovaPindorama_Fundo
        self.bgMap.draw(screen)

        # 4) OVERLAY de "00Vilarejo_Canaa_Complete" (SE concluído), SEM depender de all_sprites
        if self.overlay_vilarejo_complete and self.completed_areas_status[0]:
            screen.blit(self.overlay_vilarejo_complete, (0, 0))

        # 5) LAYER DINÂMICO da área selecionada (selected/completed)
        #    OBS: como load_area() limpou/criou sprites de área, usamos o draw padrão do Scene p/ desenhá-los agora.
        super().draw(screen)

        # 6) Cursor por cima do layer dinâmico
        self.cursor.draw(screen)

        # 7) Moldura final
        self.bg_mold.draw(screen)

       
    # -----------------------------------------------------
    #  PAUSA / SAÍDAS
    # -----------------------------------------------------
    def resume_game(self):
        print("[DEBUG] Jogo retomado.")
        self.overlay = None

    def goto_shop(self):
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")

    def goto_menu(self):
        print("[DEBUG] Retornando ao menu principal...")
        self.change_scene(Title())
   


# Criando Tela de Nível
class Level(Scene):
    """Classe para a tela de nível."""
    
    def __init__(self, player_data=None, hud_data=None): 
        super().__init__()  # Chama o construtor da classe base
        
        self.font = pygame.font.Font(None, 36)  # Fonte usada pelo menu de pausa
        
        # Criação do chão
        self.ground = Ground(0, 400, 800, 20)  # x, y, largura, altura
        self.all_sprites.add(self.ground)  # Adiciona o chão ao grupo de sprites

        # Criação dos objetos na cena - Iremos trocar por layers
        #self.img_a = Obj("assets/levelSprite/level_1_1a.png", [0, 0], [self.all_sprites])  # Fundo da fase
        self.hudbk = Hud("assets/charsSprite/player/Hud/Hud_Char_Fundo.png", [25, 25], [self.all_sprites], (640, 360))
        #self.img_b = Obj("assets/levelSprite/level_1_1b.png", [0, 0], [self.all_sprites])  # Fundo da fase
        
        # ---------- CAMADAS DO CENÁRIO (LEVEL_1_1) ----------
        self.layers = LayerStack()
        base_path = "assets/levelSprite/"

        # ORDEM: do fundo para a frente (como você definiu)

        # 1) level_1_1a (fundo absoluto) → BACK
        self.layers.add("level_1_1a",
            StaticLayer(f"{base_path}level_1_1a.png", z=0, plane="back", pos=(0,0))
        )

        # 2) level_1_1aa <-> level_1_1ab (intercalando) → BACK
        self.layers.add("level_1_1aa_ab",
            FlipLayer(f"{base_path}level_1_1aa.png", f"{base_path}level_1_1ab.png",
                    fps=4.0, z=10, plane="back", pos=(0,0))
        )

        # 3) level_1_1b → BACK
        self.layers.add("level_1_1b",
            StaticLayer(f"{base_path}level_1_1b.png", z=20, plane="back", pos=(0,0))
        )

        # 4) level_1_1c → BACK
        self.layers.add("level_1_1c",
            StaticLayer(f"{base_path}level_1_1c.png", z=30, plane="back", pos=(0,0))
        )

        # 5) level_1_1ca <-> level_1_1cb (intercalando) → BACK
        self.layers.add("level_1_1ca_cb",
            FlipLayer(f"{base_path}level_1_1ca.png", f"{base_path}level_1_1cb.png",
                    fps=5.0, z=40, plane="back", pos=(0,0))
        )

        # ==== (Player e NPC são desenhados entre back e front) ====

        # 6) level_1_1d → FRONT (após player/NPC)
        self.layers.add("level_1_1d",
            StaticLayer(f"{base_path}level_1_1d.png", z=10, plane="front", pos=(0,0))
        )

        # 7) level_1_1da <-> level_1_1db (intercalando) → FRONT
        self.layers.add("level_1_1ea_eb",
            FlipLayer(f"{base_path}level_1_1ea.png", f"{base_path}level_1_1eb.png",
                    fps=4.0, z=20, plane="front", pos=(0,0))
        )

        # 8) level_1_1ea <-> level_1_1eb (intercalando) → FRONT
        self.layers.add("level_1_1fa_fb",
            FlipLayer(f"{base_path}level_1_1fa.png", f"{base_path}level_1_1fb.png",
                    fps=5.0, z=30, plane="front", pos=(0,0))
        )

        # 9) level_1_1f → FRONT (última de todas)
        self.layers.add("level_1_1g",
            StaticLayer(f"{base_path}level_1_1g.png", z=40, plane="front", pos=(0,0))
        )

        # relógio para delta time das animações
        self._layers_last_ticks = pygame.time.get_ticks()
        # ----------------------------------------------------------
        
        
        # HUD com dados anteriores (se houver)
        self.hud = Hud("assets/charsSprite/player/Hud/Hud_Char_Contorno.png", [25, 25], [self.all_sprites], (640, 360))
        if hud_data:
            self.hud.gold = hud_data.get("gold", 0)
            self.hud.life = hud_data.get("life", 25)
            self.hud.lives = hud_data.get("lives", 3)
            self.hud.xp = hud_data.get("xp", 0)

        # Player com dados anteriores (se houver)
        if player_data:
            self.player = Player(
                image_path=player_data.get("image_path", "assets/charsSprite/player/indigenaM/R0.png"),
                position=player_data.get("position", [100, 250]),
                groups=[self.all_sprites],
                size=player_data.get("size", (200, 200)),
                life=player_data.get("life", 25),
                lives=player_data.get("lives", 3),
                xp=player_data.get("xp", 0)
            )
        else:
            self.player = Player("assets/charsSprite/player/indigenaM/R0.png", [100, 250], [self.all_sprites], (200, 200)) # O Player agora se alinha ao chão

        # Define os buracos apenas nesta fase específica
        hole_rect = pygame.Rect(520, GROUND_LEVEL-10, 100, 400)  # (x, y, largura, altura)
        self.player.set_holes([hole_rect])  # Envia os buracos para o jogador

        # Sincroniza a HUD com o Player
        self.hud.update_lives(self.player.lives)
        
        self.npc = NPC_Cacique("assets/charsSprite/npcs/Cacique/CR1.png", [1000, 285], [self.all_sprites], (200, 200)) # O NPC agora se alinha ao chão
        
        # Fonte para o ChatBox
        font = pygame.font.Font(None, 30)  # Fonte padrão
        self.chatbox = ChatBox(font, (75, 250), (800, 400))  # ChatBox na parte inferior

        # Controle de fluxo Diálogos e questões
        self.dialogue = Dialogo_1_1.falas[:5]  # Primeiro conjunto de diálogos
        self.questions = Questoes_1_1.perguntas  # Todas as questões
        self.final_dialogue = Dialogo_1_1.falas[5:]  # Últimos diálogos
        self.current_question = 0  # Índice da questão atual
        self.dialogue_stage = 0  # 0: Diálogo inicial, 1: Questões, 2: Diálogo final
        self.dialogue_finished = False  # Controle para saber se o diálogo terminou
        self.confirming_answer = False  # Indica se está no processo de confirmação
        self.selected_option = None  # Guarda a opção selecionada para confirmar
        self.exit_enabled = False  # Sinaliza quando o player pode sair para o Level_1_2
        
        # quando liberar a saída, permite que o player atravesse a borda
        setattr(self.player, "exit_mode", True)
        
        #Gold e Conversão
        self.gold_reward = 0  # Quantidade de ouro por resposta correta (ajuste conforme necessário)
        self.points_to_gold_conversion = 2  # 1 ponto = 10 Gold (ajuste conforme necessário)
        
        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)  # Embaralha as perguntas
           

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de nível."""
        # ✅ Ativa o menu de pausa com ESC
        super().handle_events(event)
        
        # ⚠️ Se o overlay estiver ativo, não processa eventos do jogo
        if self.overlay:
            return
        
        # 🎮 Eventos do jogador
        self.player.events(event)


        # 🎯 Início da lógica de interações
        if event.type == pygame.KEYDOWN:  # Certifique-se de que é um evento de tecla
            # Inicia o diálogo com o NPC
            if event.key == pygame.K_e and self.player.rect.colliderect(self.npc.rect) and not self.chatbox.is_active():
                if self.dialogue_stage == 0:  # Diálogo inicial
                    # Converte o diálogo para uma lista de strings no formato desejado
                    formatted_dialogue = [f"{speaker} {message}" for speaker, message in Dialogo_1_1.falas[:5]]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True
                elif self.dialogue_stage == 2:  # Diálogo final
                    # Limpa qualquer dado residual das questões
                    self.chatbox.options = []  # Limpa as opções
                    self.chatbox.title = ""  # Limpa o título
                    self.chatbox.question = ""  # Limpa a pergunta

                    # Exibe o diálogo final
                    formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                    self.chatbox.display_messages(formatted_dialogue)
                    self.chatbox.active = True
                    return super().handle_events(event)

            # Avança no diálogo ou responde à questão
            elif event.key == pygame.K_RETURN and self.chatbox.is_active():
                if self.chatbox.options:  # Responde à questão
                    selected_option = self.chatbox.select_option()
                    current_question = self.questions[self.current_question]
                    if selected_option == current_question["resposta_correta"]:
                        print("Resposta correta!")
                        points = current_question.get("pontos", 0)  # Obtém os pontos da questão
                        if points > 0:  # Verifica se a questão tem pontos
                            gold_reward = points * self.points_to_gold_conversion  # Converte pontos para gold
                            self.hud.update_gold(self.hud.gold + gold_reward)  # Atualiza o ouro no HUD
                            print(f"Você ganhou {gold_reward} de gold!")
                        else:
                            print("Esta questão não tem pontos definidos.")

                    else:
                        print("Resposta errada.")

                    # Avança para a próxima questão ou finaliza as perguntas
                    self.current_question += 1
                    if self.current_question < len(self.questions):
                        question_data = self.questions[self.current_question]
                        
                        # Embaralha as alternativas antes de exibi-las
                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)  # Embaralha as alternativas
                        
                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],  # Texto da pergunta
                            shuffled_options  # Alternativas embaralhadas
                        )
                    else:
                        # Finaliza as perguntas e ativa o diálogo final
                        self.dialogue_stage = 2  # Passa para o diálogo final
                        self.chatbox.options = []  # Limpa as opções
                        self.chatbox.title = ""  # Limpa o título
                        self.chatbox.question = ""  # Limpa a pergunta

                        formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True
                else:
                    self.chatbox.next_message()

                    # Quando o diálogo inicial termina, inicia as questões
                    if self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 0:
                        self.dialogue_stage = 1  # Avança para a etapa de questões
                        question_data = self.questions[self.current_question]
                        
                        # Embaralha as alternativas antes de exibi-las
                        shuffled_options = question_data["opcoes"][:]
                        random.shuffle(shuffled_options)  # Embaralha as alternativas
                        
                        self.chatbox.display_question(
                            question_data["titulo"],
                            question_data["pergunta"],
                            shuffled_options
                        )
                        self.chatbox.active = True
                        
                    # Verificar para Colocar o Score Ponts aqui, como Estágio 2 e retornar para o Diálogo como Estágio 3   

                    # Quando o diálogo final termina, desativa o chatbox
                    elif self.chatbox.current_message >= len(self.chatbox.messages) and self.dialogue_stage == 2:
                        self.chatbox.active = False
                        self.exit_enabled = True
                        
                        

            # Navegação entre opções
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.chatbox.options:
                self.chatbox.previous_option()
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.chatbox.options:
                self.chatbox.next_option()
                
    def open_pause_menu(self):
        """Abre o menu de pausa com overlay de inventário."""
        # Garante que o overlay só é criado se ainda não existir
        if not self.overlay:
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=self.on_resume,
                on_shop=self.on_shop,
                on_main_menu=self.on_main_menu
            )

    def on_resume(self):
        """Fecha o menu de pausa e retoma o jogo."""
        print("[DEBUG] Jogo retomado.")
        self.overlay = None

    def on_shop(self):
        """Ação da opção 'Escambo (Loja)'."""
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")
        # Aqui você pode trocar a cena futuramente:
        # self.change_scene(Shop())

    def on_main_menu(self):
        """Volta para a tela inicial."""
        print("[DEBUG] Retornando ao menu principal...")
        from script.scenes import Title  # Evita import circular
        self.change_scene(Title())           


    def update(self):
        
        # ---- delta-time para animações de layers ----
        now = pygame.time.get_ticks()
        if not hasattr(self, "_layers_last_ticks"):
            self._layers_last_ticks = now
        dt = (now - self._layers_last_ticks) / 1000.0
        self._layers_last_ticks = now

        self.layers.update(dt)
        # --------------------------------------------
        
        """Atualiza o estado da cena, incluindo o jogador e animações."""        
        self.player.check_death()  # <- Verifica e reduz a vida se necessário
        self.hud.update_life(self.player.life)  # Atualiza os pontos de vida
        self.hud.update_lives(self.player.lives)  # Atualiza o número de vidas
        self.hud.update_xp(self.player.xp)  # Atualiza o XP (caso necessário)
        self.player.update()  # Atualiza o jogador
        self.npc.update()  # Atualiza o NPC Cacique
        super().update()  # Atualiza os outros objetos da cena
        self.all_sprites.update()
        
        # Se o jogador concluiu o diálogo e saiu pela direita, muda de fase
        if self.exit_enabled and self.player.rect.x >= 1280:
            print("[DEBUG] Transição de fase - vidas atuais:", self.player.lives)
            self.change_scene(Level_1_2(
                player_data={
                    "image_path": self.player.image_path,
                    "position": [0, 250],
                    "size": self.player.size,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                },
                hud_data={
                    "gold": self.hud.gold,
                    "life": self.player.life,
                    "lives": self.player.lives,
                    "xp": self.player.xp
                }
        ))

        # Verifique se o jogador morreu e mude para a tela de Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())  # Muda para a cena de Game Over

    def draw(self, screen):
        """Desenha a cena e o jogador na tela."""
        screen.fill((0, 0, 0))  # Limpa a tela com fundo preto
        
        # 1) BACK (fundo e camadas intercaladas antes do player/NPC)
        self.layers.draw_back(screen)

        # 2) SPRITES (tudo que já existe nos seus grupos)
        self.all_sprites.draw(screen)

        # 3) Player e NPC explícitos (mantém seu comportamento atual)
        screen.blit(self.npc.image, self.npc.rect)
        screen.blit(self.player.image, self.player.rect)

        # 4) FRONT (camadas que ficam na frente de todos)
        self.layers.draw_front(screen)

        # 5) Disparos do player (se quer que fiquem na frente do front, deixe aqui;
        #    se quiser que fiquem "no meio", mova o loop para antes do draw_front)
        for shot in self.player.shots:
            shot.draw(screen)

        # 6) HUD (por cima de tudo)
        screen.blit(self.hud.image, self.hud.rect)

        # 7) Chatbox e Overlay (se ativos)
        self.chatbox.draw(screen)
        if self.overlay:
            self.overlay.draw(screen)

        pygame.display.update()
     
        
# Criando Tela de Nível
class Level_1_2(Level):
    """Classe para a tela de nível."""
    
    def __init__(self, player_data=None, hud_data=None): 
        super().__init__(player_data, hud_data)

        # Criação do chão
        self.ground = Ground(0, 400, 800, 20)
        self.all_sprites.add(self.ground)
        
        self.layers = LayerStack()

        # Fundo da fase
        #self.img = Obj("assets/levelSprite/level_1_2.png", [0, 0], [self.all_sprites])
        self.hudbk = Hud("assets/charsSprite/player/Hud/Hud_Char_Fundo.png", [25, 25], [self.all_sprites], (640, 360))
        
        # Criação da HUD do Boss
        self.boss_hud = BossHud("assets/charsSprite/bosses/Hud_Mapinguari.png", (0, 0), (1280, 720))
        
        self.layers = LayerStack()
        
        # ---------- CAMADAS DO CENÁRIO (LEVEL_1_2) ----------
        base_path = "assets/levelSprite/"   # use este prefixo simples (imagens na raiz de levelSprite)

        # 1) FUNDO ABSOLUTO → BACK
        self.layers.add("level_1_2a",
            StaticLayer(f"{base_path}level_1_2a.png", z=0, plane="back", pos=(0,0))
        )

        # ==== Player / Boss são desenhados entre BACK e FRONT ====

        # 4) PAR INTERCALADO → FRONT (fica NA FRENTE do player/boss)
        #    ATENÇÃO: ajuste os nomes exatamente como estão nos arquivos:
        #    se seus arquivos são "level_1_2AA.png" (AA maiúsculo) e "level_1_2ab.png", use assim:
        flip_AA = f"{base_path}level_1_2AA.png"  # ou "level_1_2aa.png" se for tudo minúsculo
        flip_ab = f"{base_path}level_1_2ab.png"

        self.layers.add("level_1_2AA_ab",
            FlipLayer(flip_AA, flip_ab, fps=4.0, z=10, plane="front", pos=(0,0))
        )

        # 5) CAMADA FRONTAL ESTÁTICA → FRONT
        self.layers.add("level_1_2b",
            StaticLayer(f"{base_path}level_1_2b.png", z=20, plane="front", pos=(0,0))
        )

        # Relógio p/ delta-time das animações de layer
        self._layers_last_ticks = pygame.time.get_ticks()

        # Criação do jogador com dados recebidos da fase anterior
        if player_data:
            self.player = Player(
                image_path=player_data.get("image_path", "assets/charsSprite/player/indigenaM/R0.png"),
                position=player_data.get("position", [100, 250]),
                groups=[self.all_sprites],
                size=player_data.get("size", (200, 200)),
                life=player_data.get("life", 25),
                lives=player_data.get("lives", 3),
                xp=player_data.get("xp", 0)
            )
        else:
            self.player = Player("assets/charsSprite/player/indigenaM/R0.png", [100, 250], [self.all_sprites], (200, 200))

        # Criação da HUD (sem valores ainda)
        self.hud = Hud("assets/charsSprite/player/Hud/Hud_Char_Contorno.png", [25, 25], [self.all_sprites], (640, 360))
        
        # Atualiza a HUD com os dados recebidos da fase anterior (se houver)
        self.hud.life = self.player.life
        self.hud.lives = self.player.lives
        self.hud.xp = self.player.xp
        if hud_data:
            self.hud.gold = hud_data.get("gold", 0)

        print("[DEBUG] Player.lives ao entrar:", self.player.lives)
        print("[DEBUG] HUD.lives após update:", self.hud.lives)

        # Boss
        self.boss = Boss_Mapinguari([850, 100], [self.all_sprites], size=(400, 400))
        
        # --- ADICIONE: flags ---
        self.boss_defeated = False
        self.exit_enabled = False

        # Fonte e chatbox
        #font = pygame.font.Font(None, 30)
        self.chatbox = None
        # Forçar para valor que nunca entra no diálogo
        self.dialogue_stage = -1
        
        self.boss_name_font = pygame.font.Font("assets/font/Primitive.ttf", 28)  # Tamanho da fonte: 40
        self.boss_name_text = self.boss_name_font.render("Mapinguari", True, (0, 0, 0))  # Branco
        self.boss_name_pos = (880, 580)  # Posição no canto superior direito (ajuste conforme a tela)
        
        self.disable_auto_exit = True  # <- impede a lógica do Level base de rodar aqui

        # Controle de diálogo e questões
        self.dialogue = Dialogo_1_1.falas[:5]
        self.questions = Questoes_1_1.perguntas
        self.final_dialogue = Dialogo_1_1.falas[5:]
        self.current_question = 0
        self.dialogue_stage = 0
        self.dialogue_finished = False
        self.confirming_answer = False
        self.selected_option = None
        self.exit_enabled = False

        self.gold_reward = 0
        self.points_to_gold_conversion = 2

        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)
        
        # Fonte de pausa
        self.font = FONT_BIG
           

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de nível (player e chatbox desacoplados)."""
        # 0) Overlay de pausa tem prioridade total
        if self.overlay:
            self.overlay.handle_events(event)
            return

        # 1) ESC abre o menu de pausa (e consome o evento)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_pause_menu()
            return

        # 2) SEMPRE repassar o evento para o Player primeiro
        #    (garante que setas/A-D/W-S etc. funcionem para o player independentemente de chatbox)
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            self.player.events(event)

        # 3) Helpers seguros para chatbox
        def cb_exists() -> bool:
            return self.chatbox is not None

        def cb_active() -> bool:
            return cb_exists() and bool(getattr(self.chatbox, "active", False))

        def cb_has_options() -> bool:
            return cb_exists() and bool(getattr(self.chatbox, "options", []))

        # 4) Ações de diálogo (somente se você realmente estiver usando chatbox)
        if event.type == pygame.KEYDOWN:
            # 4.1) Iniciar diálogo (E perto do boss), com todas as checagens
            if (event.key == pygame.K_e
                and self.player.rect.colliderect(self.boss.rect)
                and cb_exists()
                and hasattr(self.chatbox, "is_active")
                and not self.chatbox.is_active()):
                if self.dialogue_stage == 0:
                    # formata falas iniciais
                    if hasattr(self.chatbox, "display_messages"):
                        formatted_dialogue = [f"{speaker} {message}" for speaker, message in Dialogo_1_1.falas[:5]]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True
                elif self.dialogue_stage == 2:
                    # limpa resíduos + mostra falas finais
                    if cb_exists():
                        if hasattr(self.chatbox, "options"):  self.chatbox.options = []
                        if hasattr(self.chatbox, "title"):    self.chatbox.title = ""
                        if hasattr(self.chatbox, "question"): self.chatbox.question = ""
                    if hasattr(self.chatbox, "display_messages"):
                        formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                        self.chatbox.display_messages(formatted_dialogue)
                        self.chatbox.active = True

            # 4.2) Avançar diálogo / responder questão (Enter) — só se chatbox ativa
            elif event.key == pygame.K_RETURN and cb_active():
                if cb_has_options():
                    # respondendo questão
                    if hasattr(self.chatbox, "select_option"):
                        selected_option = self.chatbox.select_option()
                    else:
                        selected_option = None

                    current_question = self.questions[self.current_question]
                    if selected_option == current_question["resposta_correta"]:
                        print("Resposta correta!")
                        points = current_question.get("pontos", 0)
                        if points > 0:
                            gold_reward = points * self.points_to_gold_conversion
                            self.hud.update_gold(self.hud.gold + gold_reward)
                            print(f"Você ganhou {gold_reward} de gold!")
                        else:
                            print("Esta questão não tem pontos definidos.")
                    else:
                        print("Resposta errada.")

                    # próxima questão ou diálogo final
                    self.current_question += 1
                    if self.current_question < len(self.questions):
                        q = self.questions[self.current_question]
                        shuffled = q["opcoes"][:]
                        random.shuffle(shuffled)
                        if hasattr(self.chatbox, "display_question"):
                            self.chatbox.display_question(q["titulo"], q["pergunta"], shuffled)
                    else:
                        self.dialogue_stage = 2
                        if cb_exists():
                            if hasattr(self.chatbox, "options"):  self.chatbox.options = []
                            if hasattr(self.chatbox, "title"):    self.chatbox.title = ""
                            if hasattr(self.chatbox, "question"): self.chatbox.question = ""
                        if hasattr(self.chatbox, "display_messages"):
                            formatted_dialogue = [f"{speaker} {message}" for speaker, message in self.final_dialogue]
                            self.chatbox.display_messages(formatted_dialogue)
                            self.chatbox.active = True
                else:
                    # avançar falas
                    if hasattr(self.chatbox, "next_message"):
                        self.chatbox.next_message()

                    # terminou falas iniciais -> começa perguntas
                    if (cb_exists() and
                        hasattr(self.chatbox, "current_message") and
                        hasattr(self.chatbox, "messages") and
                        self.chatbox.current_message >= len(self.chatbox.messages) and
                        self.dialogue_stage == 0):
                        self.dialogue_stage = 1
                        q = self.questions[self.current_question]
                        shuffled = q["opcoes"][:]
                        random.shuffle(shuffled)
                        if hasattr(self.chatbox, "display_question"):
                            self.chatbox.display_question(q["titulo"], q["pergunta"], shuffled)
                            self.chatbox.active = True

                    # terminou falas finais -> libera saída
                    elif (cb_exists() and
                        hasattr(self.chatbox, "current_message") and
                        hasattr(self.chatbox, "messages") and
                        self.chatbox.current_message >= len(self.chatbox.messages) and
                        self.dialogue_stage == 2):
                        self.chatbox.active = False
                        self.exit_enabled = True
                        
                        # quando liberar a saída, permite que o player atravesse a borda
                        setattr(self.player, "exit_mode", True)

            # 4.3) Navegação da chatbox com W/S (setas continuam livres para o Player)
            elif event.key == pygame.K_w and cb_has_options():
                if hasattr(self.chatbox, "previous_option"):
                    self.chatbox.previous_option()
            elif event.key == pygame.K_s and cb_has_options():
                if hasattr(self.chatbox, "next_option"):
                    self.chatbox.next_option()

            # 4.4) Confirmar também com Espaço ou E (além de Enter)
            elif event.key in (pygame.K_SPACE, pygame.K_e) and cb_active():
                if hasattr(self.chatbox, "confirm"):
                    self.chatbox.confirm()

            # 4.5) (Opcional) fechar chatbox com ESC
            elif event.key == pygame.K_ESCAPE and cb_exists():
                # se tiver um método próprio:
                if hasattr(self, "close_dialog"):
                    self.close_dialog()
                else:
                    # fallback seguro
                    self.chatbox = None

        # 5) deixe o restante da cadeia da cena (se necessário)
    #    return super().handle_events(event)
        
    def open_pause_menu(self):
        """Abre o menu de pausa com overlay de inventário."""
        if not self.overlay:
            from script.setting import FONT_BIG, FONT_SMALL  # ✅ deve importar aqui também
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=self.on_resume,
                on_shop=self.on_shop,
                on_main_menu=self.on_main_menu
            )

    def on_resume(self):
        print("[DEBUG] Jogo retomado.")
        self.overlay = None

    def on_shop(self):
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")

    def on_main_menu(self):
        print("[DEBUG] Retornando ao menu principal...")
        from script.scenes import Title
        self.change_scene(Title())    

    def update(self):
        # ---- delta-time para animações de layer ----
        now = pygame.time.get_ticks()
        dt = (now - getattr(self, "_layers_last_ticks", now)) / 1000.0
        self._layers_last_ticks = now
        self.layers.update(dt)
        # --------------------------------------------

        # HUD do player
        self.hud.update_life(self.player.life)
        self.hud.update_lives(self.player.lives)
        self.hud.update_xp(self.player.xp)

        # Atualizações padrões (groups etc.)
        super().update()

        # --- 1 HIT KILL: tiro do player acertou o boss? ---
        if not getattr(self, "boss_defeated", False):
            for shot in list(self.player.shots):
                if shot.rect.colliderect(self.boss.rect):
                    self.boss_defeated = True
                    self.exit_enabled = True
                    setattr(self.player, "exit_mode", True) # ← permite cruzar a borda
                    self._auto_exit = True  # ativa auto-walk
                    
                    try:
                        self.boss.kill()   # remove do all_sprites se estiver nele
                    except Exception:
                        pass
                    shot.kill()
                    break

        # --- sair pela direita -> volta para o mapa e marca a área como concluída ---
        if self.exit_enabled and self.player.rect.x >= 1280:
            # marca a área desta fase como concluída (persistido em memória do módulo)
            WORLD_PROGRESS["areas_done"].add("Level_1_2")

            # volta para a tela de mapa
            self.change_scene(Map())

        # Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())

    def draw(self, screen):
        """Desenha a cena e o jogador na tela."""
        screen.fill((0, 0, 0))  # Limpa a tela com fundo preto

        # 1) FUNDO -> desenha apenas os layers 'back' (aqui entra o Level_1_2a)
        #    (garanta no __init__ que você registrou: StaticLayer("level_1_2a", plane="back"))
        self.layers.draw_back(screen)

        # 2) PLAYER
        screen.blit(self.player.image, self.player.rect)

        # 3) BOSS (logo após o player)
        if not getattr(self, "boss_defeated", False):
            screen.blit(self.boss.image, self.boss.rect)

        # 4) LAYERS FRONTAIS -> par intercalado (AA<->ab) e depois a estática 'b'
        #    (ambos devem ter plane="front" no __init__)
        self.layers.draw_front(screen)

        # 5) Disparos do player (se quer que fiquem ATRÁS das máscaras frontais,
        #    mova este bloco para ANTES de self.layers.draw_front(screen))
        for shot in self.player.shots:
            shot.draw(screen)

        # 6) HUD do Player
        screen.blit(self.hud.image, self.hud.rect)

        # 7) HUD do Boss (por último)
        if not getattr(self, "boss_defeated", False):
            screen.blit(self.boss_hud.image, self.boss_hud.rect)
            screen.blit(self.boss_name_text, self.boss_name_pos)

        # 8) Overlay (se ativo)
        if self.overlay:
            self.overlay.draw(screen)

        pygame.display.update()
           
               
# Criando Tela de Game Over
class GameOver(Scene):
    """Classe para a tela de Game Over."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        self.img = Obj("assets/gameOver.png", [0, 0], [self.all_sprites])  # Carrega a imagem de Game Over
        
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de Game Over."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.change_scene(Title())  # Muda para a tela inicial            
        return super().handle_events(event)
    
    def draw(self, surface):
        """Desenha a tela de Game Over."""
        self.img.draw(surface)
    

