import pygame
pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Тестовый проект")

image = pygame.image.load("picPython.png")
image_rect = image.get_rect()



run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            image_rect.x = mouseX - 40
            image_rect.y = mouseY - 40







    screen.fill((0, 0, 0))
    screen.blit(image, image_rect)
    pygame.display.flip()

pygame.quit()
