import pygame, sys
from settings import *
from menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Tales of the Great Warrior")
        self.click = False

        self.menu = Menu()


    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False


            self.screen.fill('green')

            self.menu.mainmenu(self.click)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.game_loop()




