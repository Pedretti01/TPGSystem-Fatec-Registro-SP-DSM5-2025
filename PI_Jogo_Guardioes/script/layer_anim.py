# layer_anim.py
import pygame
from typing import Dict, Optional, Tuple

# --------------------------------------------------------------
# 🔹 CLASSE BASE: serve de modelo para qualquer tipo de layer.
# --------------------------------------------------------------
class BaseLayer:
    def __init__(self, z: int, plane: str = "back",
                 pos: Tuple[int, int] = (0, 0),
                 alpha: Optional[int] = None):
        """
        z: controla a ordem de desenho dentro do plano (menor = atrás)
        plane: define o plano de exibição ("back" = atrás do player, "front" = na frente)
        pos: posição (x, y) onde a camada será desenhada
        alpha: transparência opcional (0 = invisível, 255 = opaco)
        """
        assert plane in ("back", "front")
        self.z = z
        self.plane = plane
        self.pos = list(pos)
        self.alpha = alpha
        self.visible = True  # pode desligar um layer sem removê-lo

    # Essas funções são sobrescritas nas classes filhas
    def update(self, dt: float): ...
    def draw(self, surface: pygame.Surface): ...


# --------------------------------------------------------------
# 🔹 CAMADA ESTÁTICA: exibe uma imagem fixa (sem animação)
# --------------------------------------------------------------
class StaticLayer(BaseLayer):
    """
    Representa uma camada estática (sem troca de frames).
    Exemplo: montanhas, céu, chão fixo etc.
    """
    def __init__(self, image_path: str, z: int,
                 plane: str = "back", pos=(0, 0),
                 alpha: Optional[int] = None,
                 scale: Optional[Tuple[int, int]] = None):
        super().__init__(z, plane, pos, alpha)

        # Carrega a imagem do disco
        img = pygame.image.load(image_path).convert_alpha()

        # Redimensiona, se necessário
        if scale:
            img = pygame.transform.smoothscale(img, scale)

        # Define transparência (opcional)
        if alpha is not None:
            img.set_alpha(alpha)

        # Guarda a imagem pronta para desenhar
        self.image = img

    def draw(self, surface: pygame.Surface):
        """Desenha a imagem, se estiver visível."""
        if self.visible:
            surface.blit(self.image, self.pos)


# --------------------------------------------------------------
# 🔹 CAMADA ANIMADA (FlipLayer)
# --------------------------------------------------------------
class FlipLayer(BaseLayer):
    """
    Camada que alterna entre duas imagens (frame A e frame B).
    Serve para efeitos simples de animação (ex: ondas, cachoeira, folhas balançando).
    """
    def __init__(self, img_a: str, img_b: str, fps: float, z: int,
                 plane: str = "back", pos=(0, 0),
                 alpha: Optional[int] = None,
                 scale: Optional[Tuple[int, int]] = None,
                 start_on_b: bool = False):
        """
        img_a / img_b: caminhos das imagens que vão intercalar.
        fps: quantas vezes por segundo a troca acontece (8 → troca 8x por segundo).
        z, plane, pos, alpha: mesmos parâmetros do BaseLayer.
        start_on_b: define se começa exibindo a segunda imagem.
        """
        super().__init__(z, plane, pos, alpha)

        # Carrega e prepara as duas imagens
        a = pygame.image.load(img_a).convert_alpha()
        b = pygame.image.load(img_b).convert_alpha()
        if scale:
            a = pygame.transform.smoothscale(a, scale)
            b = pygame.transform.smoothscale(b, scale)
        if alpha is not None:
            a.set_alpha(alpha)
            b.set_alpha(alpha)

        # Guarda os dois frames
        self.frames = [a, b]

        # Define a velocidade da animação
        self.fps = max(0.0, fps)
        self._time = 0.0  # tempo acumulado
        self._index = 1 if start_on_b else 0  # começa com o frame A ou B

    # --- métodos de controle ---
    def set_images(self, img_a: str, img_b: str, keep_phase: bool = True):
        """
        Troca as imagens A e B em tempo de execução (ex: mudar para versão noturna).
        keep_phase=True mantém o quadro atual (não reseta a animação).
        """
        idx = self._index
        a = pygame.image.load(img_a).convert_alpha()
        b = pygame.image.load(img_b).convert_alpha()
        if self.alpha is not None:
            a.set_alpha(self.alpha)
            b.set_alpha(self.alpha)
        self.frames = [a, b]

        if not keep_phase:
            # reinicia a animação
            self._index = 0
            self._time = 0.0
        else:
            # mantém o mesmo quadro atual
            self._index = idx

    def set_fps(self, fps: float):
        """Altera a velocidade da animação."""
        self.fps = max(0.0, fps)

    def update(self, dt: float):
        """
        Atualiza o tempo e alterna entre as imagens
        com base no 'fps' (quadros por segundo).
        """
        if not self.visible or self.fps <= 0:
            return

        # soma o tempo desde o último update
        self._time += dt
        frame_time = 1.0 / self.fps  # tempo por quadro

        # alterna entre A e B quando passar o tempo do frame
        while self._time >= frame_time:
            self._time -= frame_time
            self._index ^= 1  # troca 0 ↔ 1

    def draw(self, surface: pygame.Surface):
        """Desenha o frame atual na tela."""
        if self.visible:
            surface.blit(self.frames[self._index], self.pos)


# --------------------------------------------------------------
# 🔹 LAYERSTACK — Gerencia todas as camadas do cenário
# --------------------------------------------------------------
class LayerStack:
    """
    O LayerStack é o gerenciador principal das camadas:
      - Guarda todas as camadas registradas.
      - Atualiza todas (para animar FlipLayers).
      - Desenha na ordem correta de fundo e frente.
    """
    def __init__(self):
        # Dicionário que armazena os layers por nome
        self._layers: Dict[str, BaseLayer] = {}

    def add(self, name: str, layer: BaseLayer):
        """Adiciona um novo layer ao stack e o identifica por nome."""
        self._layers[name] = layer
        return layer  # retorna o próprio objeto para uso direto se quiser

    def get(self, name: str) -> Optional[BaseLayer]:
        """Retorna o layer pelo nome (útil para alterar propriedades depois)."""
        return self._layers.get(name)

    def update(self, dt: float):
        """Atualiza todas as camadas (importante para animar as FlipLayers)."""
        for ly in self._layers.values():
            ly.update(dt)

    def draw_back(self, surface: pygame.Surface):
        """Desenha apenas as camadas que estão atrás do player (plane='back')."""
        # ordena por z para manter a profundidade correta
        for ly in sorted(
            (l for l in self._layers.values() if l.plane == "back"),
            key=lambda L: L.z
        ):
            ly.draw(surface)

    def draw_front(self, surface: pygame.Surface):
        """Desenha apenas as camadas da frente (plane='front')."""
        for ly in sorted(
            (l for l in self._layers.values() if l.plane == "front"),
            key=lambda L: L.z
        ):
            ly.draw(surface)
