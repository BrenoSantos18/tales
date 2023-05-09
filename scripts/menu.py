import pygame, sys, time
from settings import *
from maps import Level



class Menu:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.level = Level()
        self.font = pygame.font.SysFont('arielblack', 40)
        self.in_menu = False

        self.click = False
        self.event = False
        self.event_time = 0
        self.event_cooldown = 500


    def get_event_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.event_time >= self.event_cooldown:
            self.event = False


    def mainmenu(self, click):

        #button
        mx, my = pygame.mouse.get_pos()
        menu_bg = pygame.image.load('Assets/Imagens/menu/main_menu.png')
        menu_rect = menu_bg.get_rect(topleft = (0,0))

        start_game = pygame.Rect(48,113,432,81)
        quit = pygame.Rect(48,385, 432,81)
        pygame.draw.rect(self.screen, 'grey', start_game)
        pygame.draw.rect(self.screen, 'grey', quit)
        self.screen.blit(menu_bg, menu_rect)


        if start_game.collidepoint((mx, my)) and click:
            self.game_run()


        elif quit.collidepoint(mx, my) and click:
            pygame.quit()
            sys.exit()




    def game_run(self):
        previous_time = time.time()
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()

            self.get_event_cooldown()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.event:
                        self.event = True
                        self.event_time = pygame.time.get_ticks()
                        self.click = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.event:
                        self.event = True
                        self.event_time = pygame.time.get_ticks()
                        if not self.in_menu:
                            self.in_menu = True
                        else:
                            self.in_menu = False


            self.level.draw(dt)

            if self.in_menu:
                self.pause_box()

            pygame.display.update()


    def pause_box(self):
        mx, my = pygame.mouse.get_pos()

        pause_menu = pygame.image.load('Assets/Imagens/menu/pause.png')
        pause_rect = pause_menu.get_rect(topleft = (screen_width/2-250, screen_height/2-200))

        #rects background
        self.screen.blit(pause_menu, pause_rect)

        resume_rect = pygame.Rect(screen_width/2-200,screen_height/2 - 179,400,50)

        quit_rect = pygame.Rect(screen_width/2-200,screen_height/2+70,400,50)

        if resume_rect.collidepoint((mx,my)):
            self.in_menu = False
        if quit_rect.collidepoint((mx,my)):
            if self.click:
                pygame.quit()
                sys.exit()









