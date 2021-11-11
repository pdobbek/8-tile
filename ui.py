import pygame

def main():
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal_program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((240, 180))

    # define a variable to control the main loop
    is_running = True

    # main loop
    while is_running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False to exit the main loop
                is_running = False


if __name__ == '__main__':
    main()
