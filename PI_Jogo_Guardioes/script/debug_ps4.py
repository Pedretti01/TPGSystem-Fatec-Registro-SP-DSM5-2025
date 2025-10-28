import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Nenhum controle detectado!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Controle detectado: {joystick.get_name()}")
print(f"Botões: {joystick.get_numbuttons()}")
print(f"Eixos: {joystick.get_numaxes()}")
print(f"Hats: {joystick.get_numhats()}")

# Loop de debug
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mostra quando algum botão é pressionado
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"[PRESS] Botão {event.button}")

        if event.type == pygame.JOYBUTTONUP:
            print(f"[RELEASE] Botão {event.button}")

        # Mostra quando o D-Pad (hat) é usado
        if event.type == pygame.JOYHATMOTION:
            print(f"[HAT] {event.value}")

        # Mostra valores dos analógicos
        if event.type == pygame.JOYAXISMOTION:
            print(f"[AXIS {event.axis}] = {event.value:.2f}")