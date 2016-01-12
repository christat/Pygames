import pygame

class Barrier(pygame.sprite.Sprite):

    def __init__(self, img, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = img
        self.rect = pygame.rect.Rect(pos, self.image.get_size())

class Paddle(pygame.sprite.Sprite):

    def __init__(self, img, pos, vel, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.vel = vel
        self.image = img
        self.rect = pygame.rect.Rect(pos, self.image.get_size())

    def collider(self, game):
        #barrier handling
        for barrier in pygame.sprite.spritecollide(self, game.barriers, False):
            barrier_rect = barrier.rect
            if self.rect.y <= barrier.image.get_height():
                self.rect.y = barrier.image.get_height() + 2
            elif self.rect.y + self.image.get_height() >= barrier_rect.y:
                self.rect.y = barrier_rect.y - self.image.get_height() - 2

    def update(self, dt, game):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.y -= self.vel * dt
        if key[pygame.K_DOWN]:
            self.rect.y += self.vel * dt
        self.collider(game)


#AI Paddle, same as paddle but with pseudo AI for updating position
class AIPaddle(pygame.sprite.Sprite):
    
    def __init__(self, img, pos, *groups):
        Paddle.__init__(self, img, pos, *groups)

    def update(self, dt, game):
            #update only if ball in AI half
            if game.ball.rect.x > 400:
                prev = self.rect.copy()

                #Try to reach ball if outside vertical scope
                if game.ball.rect.y >= self.rect.y + self.image.get_height():
                    self.rect.y += self.vel * dt
                elif game.ball.rect.y + game.ball.image.get_height() <= self.rect.y:
                    self.rect.y -= self.vel * dt
                
                Paddle.collider(self, game)

class Ball(pygame.sprite.Sprite):

    def __init__(self, img, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.velx = 600
        self.vely = 0
        self.image = img
        self.rect = pygame.rect.Rect(pos, self.image.get_size())

    def update(self, dt, game):

        prev = self.rect.copy()
        self.rect.x += self.velx * dt
        self.rect.y += self.vely * dt
        #compare updated ball position with colliding paddles
        dirChanged = False
        
        for paddle in pygame.sprite.spritecollide(self, game.paddles, False):
            if not dirChanged:
                dirChanged = True
                paddle_rect = paddle.rect
                paddle_w, paddle_h = paddle.image.get_size()
                self_w = self.image.get_width()

                if prev.x <= paddle_rect.x:
                    self.rect.x = paddle_rect.x - self_w - 2
                if prev.x >= paddle_rect.x + paddle_w:
                    self.rect.x = paddle_rect.x + paddle_w + 2
               
                self.velx = -self.velx

                #Split outcome into 5 areas for different angles
                if self.rect.y <= paddle_rect.y + paddle_h/5:
                    self.vely = -600
                elif self.rect.y <= paddle_rect.y + 2*paddle_h/5:
                    self.vely = -300
                elif self.rect.y <= paddle_rect.y + 3*paddle_h/5:
                    self.vely = 0
                elif self.rect.y <= paddle_rect.y + 4*paddle_h/5:
                    self.vely = 300
                else:
                    self.vely = 600
        #handle collisions with barriers
        dirChanged = False
        for barrier in pygame.sprite.spritecollide(self, game.barriers, False):
            if not dirChanged:
                dirChanged = True
                barrier_rect = barrier.rect
                barrier_h = barrier.image.get_height()

                if prev.y <= barrier_rect.y:
                    self.rect.y = barrier_rect.y - self.image.get_height() - 2
                elif prev.y >= barrier_h:
                    self.rect.y = barrier_h + 2
                self.vely = (-1)*self.vely
            

#END
