import pygame

class Controller:
    """
    Classe Controller compatível com Xbox 360 e PS4 (DualShock 4).
    Faz o mapeamento do controle USB para eventos de teclado (KEYDOWN/KEYUP),
    permitindo que o jogo use a mesma lógica já existente do teclado.

    Funcionalidades mapeadas:
      - Direcional (↑ ↓ ← →)
      - Ataque → Q
      - Pulo → Espaço
      - Defesa → K
      - Roll/Dash → Shift Esquerdo
      - Interagir → E
      - Share → Esc
      - Options → Enter
    """

    def __init__(self):
        pygame.joystick.init()
        self.joystick = None
        self.button_map = {}
        self.dpad_map = {}

        if pygame.joystick.get_count() > 0:
            # Usa o primeiro controle conectado
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            name = self.joystick.get_name()
            print(f"[JOYSTICK] Detectado: {name}")

            # Detecta tipo de controle
            if "Wireless Controller" in name or "PS4" in name:
                self._map_ps4()
            else:
                self._map_xbox()
        else:
            print("[JOYSTICK] Nenhum controle encontrado")

        # Estado dos direcionais (para não floodar eventos)
        self.dpad_state = {"up": False, "down": False, "left": False, "right": False}

    # -----------------------
    # Mapas de botões
    # -----------------------
    def _map_xbox(self):
        """Mapeamento padrão para Xbox 360"""
        self.button_map = {
            0: pygame.K_SPACE,      # A → Espaço (Pulo)
            1: pygame.K_LSHIFT,     # B → Roll/Dash
            2: pygame.K_q,          # X → Ataque
            3: pygame.K_k,          # Y → Defesa
            4: pygame.K_e,          # LB → Interagir
            6: pygame.K_ESCAPE,     # Back → Esc
            7: pygame.K_RETURN,     # Start → Enter
        }
        # D-Pad via HAT
        self.dpad_map = {"hat": True}
        print("[MAPEAMENTO] Xbox 360 carregado")

    def _map_ps4(self):
        """Mapeamento do DualShock 4 (baseado no debug fornecido)"""
        self.button_map = {
            0: pygame.K_SPACE,      # Cross (X) → Espaço (Pulo)
            1: pygame.K_LSHIFT,     # Circle (O) → Roll/Dash
            2: pygame.K_q,          # Square (☐) → Ataque
            3: pygame.K_k,          # Triangle (Δ) → Defesa
            4: pygame.K_ESCAPE,     # Share → Esc
            6: pygame.K_RETURN,     # Options → Enter
            9: pygame.K_e,          # L1 → Interagir (corrigido)
        }
        # D-Pad via BOTÕES (11–14)
        self.dpad_map = {
            11: pygame.K_UP,
            12: pygame.K_DOWN,
            13: pygame.K_LEFT,
            14: pygame.K_RIGHT,
        }
        print("[MAPEAMENTO] PS4 carregado")

    # -----------------------
    # Posta eventos de teclado
    # -----------------------
    def _post_key(self, key, down: bool):
        """Envia evento de teclado para a fila do pygame"""
        if key is None:
            return
        evt_type = pygame.KEYDOWN if down else pygame.KEYUP
        pygame.event.post(pygame.event.Event(evt_type, {"key": key}))

    # -----------------------
    # Processa eventos do joystick
    # -----------------------
    def process_event(self, event):
        # ---------------------
        # D-Pad no PS4 (botões 11–14)
        # ---------------------
        if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
            if event.button in self.dpad_map:  # Direcional do PS4
                key = self.dpad_map[event.button]
                self._post_key(key, event.type == pygame.JOYBUTTONDOWN)

            elif event.button in self.button_map:  # Botões de ação
                self._post_key(self.button_map[event.button],
                               event.type == pygame.JOYBUTTONDOWN)

        # ---------------------
        # D-Pad no Xbox (via HAT)
        # ---------------------
        if self.dpad_map.get("hat") and event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value

            # CIMA
            if hat_y == 1 and not self.dpad_state["up"]:
                self._post_key(pygame.K_UP, True)
                self.dpad_state["up"] = True
            if hat_y != 1 and self.dpad_state["up"]:
                self._post_key(pygame.K_UP, False)
                self.dpad_state["up"] = False

            # BAIXO
            if hat_y == -1 and not self.dpad_state["down"]:
                self._post_key(pygame.K_DOWN, True)
                self.dpad_state["down"] = True
            if hat_y != -1 and self.dpad_state["down"]:
                self._post_key(pygame.K_DOWN, False)
                self.dpad_state["down"] = False

            # ESQUERDA
            if hat_x == -1 and not self.dpad_state["left"]:
                self._post_key(pygame.K_LEFT, True)
                self.dpad_state["left"] = True
            if hat_x != -1 and self.dpad_state["left"]:
                self._post_key(pygame.K_LEFT, False)
                self.dpad_state["left"] = False

            # DIREITA
            if hat_x == 1 and not self.dpad_state["right"]:
                self._post_key(pygame.K_RIGHT, True)
                self.dpad_state["right"] = True
            if hat_x != 1 and self.dpad_state["right"]:
                self._post_key(pygame.K_RIGHT, False)
                self.dpad_state["right"] = False

        return None
