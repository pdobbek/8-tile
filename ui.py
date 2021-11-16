import pygame as pg
import pygame.font

FPS = 30
TILESIZE = 120
GRIDWIDTH = 3
GRIDHEIGHT = 3
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT

BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)
MEDIUMGRAY = (80, 80, 80)
LIGHTGRAY = (180, 180, 180)


def draw_grid(screen):
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_puzzle(state, screen):
    """
    :param screen: pygame.display
    :param state: [[1, 2, 3], [4, 5, 6], [7, 8, 0]] etc.
    :return:
    """
    for i in range(len(state)):
        for j in range(len(state[i])):
            num = state[j][i]
            # draw light gray rectangle
            rect = pg.Rect((i*TILESIZE, j*TILESIZE), (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
            if num != 0:
                # draw number
                text_surface_object = pg.font.SysFont('arial', 50).render(str(num), True, BLACK)
                text_rect = text_surface_object.get_rect(center=rect.center)
                screen.blit(text_surface_object, text_rect)


def main():
    pg.init()
    # load and set the logo
    logo = pg.image.load("logo32x32.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("8-tile Puzzle")

    # create a surface on screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # define a variable to control the main loop
    is_running = True

    # main loop
    while is_running:
        clock.tick(FPS)
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    is_running = False
        draw_puzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]], screen)
        draw_grid(screen)
        pg.display.flip()


if __name__ == '__main__':
    main()
