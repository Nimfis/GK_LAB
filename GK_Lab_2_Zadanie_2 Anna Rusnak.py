import pygame

pygame.init()
# Utworzenie okna 600x600 px
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Anna Rusnak zad. 2")

# Kolory
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Zakolorowanie okna aplikacji na biało
win.fill(WHITE)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # 1. Kwadrat + koło
    pygame.draw.circle(win, BLACK, (150, 150), 100, 100)
    pygame.draw.rect(win, YELLOW, (100, 100, 100, 100))
    
    # 2. Trójkąty
    # pygame.draw.polygon(win, BLUE, [(100, 325), (150, 325), (125, 375)])
    # pygame.draw.rect(win, BLUE, (75, 375, 100, 50))
    # pygame.draw.polygon(win, BLUE, [(100, 475), (150, 475), (125, 425)])
    
    # 3. Litera Z
    # pygame.draw.rect(win, RED, (350, 350, 200, 10))
    # pygame.draw.line(win, RED, (550, 355), (350, 505), 10)
    # pygame.draw.rect(win, RED, (350, 500, 200, 10))

    pygame.display.update()
    
pygame.quit()