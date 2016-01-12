import pygame, os
from sprites import *

class Game(object):
    
    def main_menu(self, clock, screen):
        FPS = 15
        width, height = screen.get_size()

        bg = pygame.image.load(os.path.join("sprites", "menu_bg.png")).convert()
        btn_play = pygame.image.load(os.path.join("sprites", "menu_play.png")).convert_alpha()
        btn_quit = pygame.image.load(os.path.join("sprites", "menu_quit.png")).convert_alpha()
        btn_play_h = pygame.image.load(os.path.join("sprites", "menu_play_h.png")).convert_alpha()
        btn_quit_h = pygame.image.load(os.path.join("sprites", "menu_quit_h.png")).convert_alpha()


        pos_btn1 = (4*width/5, height/2 - 15)
        pos_btn2 = (0, height - btn_quit.get_height())
        opt = 0

        exit = False
        while not exit:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        opt -= 1
                    if event.key == pygame.K_DOWN:
                        opt += 1
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                    if event.key == pygame.K_RETURN:
                        if opt == 0:
                            self.Main(clock, screen)
                        else:
                            pygame.quit()
                            quit()

            #limit options
            if opt > 1:
                opt = 0
            elif opt <0:
                opt = 1
            
            #paint stuff on screen
            screen.blit(bg, (0,0))
            if opt == 0:
                screen.blit(btn_play_h, pos_btn1)
                screen.blit(btn_quit, pos_btn2)
            elif opt == 1:
                screen.blit(btn_play, pos_btn1)
                screen.blit(btn_quit_h, pos_btn2)

            pygame.display.flip()            
            clock.tick(FPS)

    def translucid_menu(self, clock, pl, ai, pausemode, screen):
        FPS = 15
        width, height = screen.get_size()
        
        #load images
        bg = pygame.image.load(os.path.join("sprites", "replay_bg.png")).convert_alpha()
        replay_img = pygame.image.load(os.path.join("sprites", "btn_replay.png")).convert()
        exit_img = pygame.image.load(os.path.join("sprites", "btn_exit.png")).convert()
        replay_img_h = pygame.image.load(os.path.join("sprites", "btn_replay_hover.png")).convert()
        exit_img_h = pygame.image.load(os.path.join("sprites", "btn_exit_hover.png")).convert()
        continue_img = pygame.image.load(os.path.join("sprites", "btn_continue.png")).convert() 
        continue_img_h = pygame.image.load(os.path.join("sprites", "btn_continue_hover.png")).convert()

        opt = 0
        btn_width = exit_img_h.get_width()
        text = None
        #initial painting of stuff
        screen.blit(bg, (0,0))
        if pausemode:
            text = self.font.render("PAUSED", True, (255,255,255))
        else:
            text = self.font.render("GAME OVER", True, (255,255,255))
            if pl > ai:
                text = self.font.render("YOU WIN! <3", True, (255,255,255))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - 50))
        
        pos_btn1 = (width/2 - btn_width/2, height/2 + 100)
        pos_btn2 = (width/2 - btn_width/2, height/2 +200)
        
        exit = False
        while not exit:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        opt -= 1
                    if event.key == pygame.K_DOWN:
                        opt += 1
                    if pausemode and event.key == pygame.K_ESCAPE:
                        exit = True
                    if event.key == pygame.K_RETURN:
                        if opt == 0:
                            if pausemode:
                                exit = True
                            else:
                                self.Main(clock, screen)
                        else:
                            pygame.quit()
                            quit()

            #limit options
            if opt > 1:
                opt = 0
            elif opt <0:
                opt = 1

            #paint stuff on screen
            if opt == 0:
                if pausemode:
                    screen.blit(continue_img_h, pos_btn1)
                    screen.blit(exit_img, pos_btn2)
                else:
                    screen.blit(replay_img_h, pos_btn1)
                    screen.blit(exit_img, pos_btn2)
            elif opt == 1:
                if pausemode:
                    screen.blit(continue_img, pos_btn1)
                    screen.blit(exit_img_h, pos_btn2)
                else:
                    screen.blit(replay_img, pos_btn1)
                    screen.blit(exit_img_h, pos_btn2)

            pygame.display.flip()            
            clock.tick(FPS)


    def Main(self, clock, screen):
        FPS = 90
        MAX_SCORE = 7
        screenx, screeny = screen.get_size()
        
        #load images
        background = pygame.image.load(os.path.join("sprites", "background.png")).convert()
        pad_img = pygame.image.load(os.path.join("sprites", "paddle.png")).convert()
        pad_ai_img = pygame.image.load(os.path.join("sprites", "ai_paddle.png")).convert()
        ball_img = pygame.image.load(os.path.join("sprites", "ball.png")).convert_alpha()
        barr_img = pygame.image.load(os.path.join("sprites", "barrier.png")).convert_alpha()
        self.font = pygame.font.Font(os.path.join("fonts", "Cantarell-Regular.ttf"), 50)
        fontcolor_l = (114,114,114)
        fontcolor_r = (255,255,255)

        #Init sprite groups (used for rectcollider and draw);
        self.sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()

        #Init sprite objects
        self.player = Paddle(pad_img, (pad_img.get_width(), screeny/2 - pad_img.get_height()/2), 700, (self.sprites, self.paddles))
        self.ai = AIPaddle(pad_ai_img, (screenx - 2*pad_ai_img.get_width(), screeny/2 - pad_ai_img.get_height()/2), 680, (self.sprites, self.paddles))
        self.ball = Ball(ball_img, (screenx/2 - ball_img.get_width()/2, screeny/2 - ball_img.get_height()/2), (self.sprites))
        self.topbarrier = Barrier(barr_img, (0,0),(self.barriers, self.sprites))
        self.bottombarrier = Barrier(barr_img, (0,screeny - barr_img.get_height()), (self.barriers, self.sprites))
        
        #game loop cond
        running = True

        #score vars
        score, score_ai = 0, 0
        reset ,score_set = False, False
        
        while running:
            dt = clock.tick(FPS)
    
            #handle quit; REWRITE AFTER FINISHED!
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.translucid_menu(clock, score, score_ai, True, screen)

            #Update sprite positions, implemented per class
            self.sprites.update(dt/1000.0, self)
            
            #update scores
            if not score_set:
                if self.ball.rect.x + ball_img.get_width() <=0:
                    score_ai += 1
                    score_set = True
                elif self.ball.rect.x >= screenx:
                    score += 1
                    score_set = True

            #reset ball if reaches boundaries (outside window)
            if self.ball.rect.x <= -screenx or self.ball.rect.x + ball_img.get_width() >= screeny+screenx:
                reset = True
                
            #reset ball and paddles
            if reset:
                self.ball.rect.x = screenx/2 - self.ball.image.get_width()/2
                self.ball.rect.y = screeny/2 - self.ball.image.get_height()/2
                self.player.rect.y = screeny/2 - self.player.image.get_height()/2
                self.ai.rect.y = screeny/2 - self.ai.image.get_height()/2
                self.ball.vely = 0
                self.ball.velx = -self.ball.velx
                reset = False
                score_set = False

            #draw evetything on screen; flip buffer
            screen.blit(background, (0,0))
            score_left = self.font.render(str(score), True, fontcolor_l)
            score_right = self.font.render(str(score_ai), True, fontcolor_r)
            screen.blit(score_left, (screenx/4, 40))
            screen.blit(score_right, (screenx - screenx/4, 40))
            self.sprites.draw(screen)
            pygame.display.flip()

            #If score reached, display replay options
            if score == MAX_SCORE or score_ai == MAX_SCORE:
                self.translucid_menu(clock, score, score_ai, False, screen)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("FlatPong")
    icon = pygame.image.load(os.path.join("sprites", "menu_play.png")).convert_alpha()
    pygame.display.set_icon(icon)
    clk = pygame.time.Clock()
    Game().main_menu(clk, screen)
    pygame.quit()
    quit()
