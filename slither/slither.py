import pygame
import time
import random

status = pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
background = (45,45,45)
snake_color = (175,215,0)
golden = (215,215,135)
purple = (175,135,235)
red = (255,0,95)

display_width = 1280
display_height = 800
game_icon = pygame.image.load('sprites/gameicon.png')
pygame.display.set_icon(game_icon)
s_head = pygame.image.load('sprites/s_head.png')
s_tail = pygame.image.load('sprites/s_tail.png')
s_body = pygame.image.load('sprites/s_body.png')
apl = pygame.image.load('sprites/apl.png')
s_corner = pygame.image.load('sprites/s_corner.png')

gameDisplay = pygame.display.set_mode((display_width,display_height), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Slither')
clock = pygame.time.Clock()
apl_thickness = 30

sfont = pygame.font.Font('fonts/Cantarell-Regular.ttf', 25)
mfont = pygame.font.Font('fonts/Cantarell-Regular.ttf', 40)
lfont = pygame.font.Font('fonts/Cantarell-Bold.ttf', 80)
xsfont = pygame.font.Font('fonts/Cantarell-Regular.ttf', 16)
def score(score):
    text = sfont.render("Score: "+str(score), True, golden)
    gameDisplay.blit(text, (0,0))

def snake(snakelist, block_size):

        s_head_rot = s_head
        if snakelist[-1][0] - snakelist[-2][0] > 0:
            s_head_rot = pygame.transform.rotate(s_head_rot, 270)
        elif snakelist[-1][0] - snakelist[-2][0] < 0:
            s_head_rot = pygame.transform.rotate(s_head_rot, 90)
        elif snakelist[-1][1] - snakelist[-2][1] > 0:
            s_head_rot = pygame.transform.rotate(s_head_rot, 180)
        
        s_tail_rot = s_tail
        if snakelist[1][0] - snakelist[0][0] > 0:
            s_tail_rot = pygame.transform.rotate(s_tail_rot, 270)
        elif snakelist[1][0] - snakelist[0][0] < 0:
            s_tail_rot = pygame.transform.rotate(s_tail_rot, 90)
        elif snakelist[1][1] - snakelist[0][1] > 0:
            s_tail_rot = pygame.transform.rotate(s_tail_rot, 180)

        for i in range(1, len(snakelist)-1):
            s_body_rot = s_body
            s_corner_rot = s_corner
            corner = False

            if snakelist[i-1][0] < snakelist[i][0] and snakelist[i+1][1] < snakelist[i][1]:
                corner = True
            elif snakelist[i-1][0] < snakelist[i][0] and snakelist[i+1][1] >  snakelist[i][1]:
                s_corner_rot = pygame.transform.rotate(s_corner_rot, 90)
                corner = True
            elif snakelist[i-1][0] > snakelist[i][0] and snakelist[i+1][1] < snakelist[i][1]:
                s_corner_rot = pygame.transform.rotate(s_corner_rot, 270)
                corner = True
            elif snakelist[i-1][0] > snakelist[i][0] and snakelist[i+1][1] > snakelist[i][1]:
                s_corner_rot = pygame.transform.rotate(s_corner_rot, 180)
                corner = True
            elif snakelist[i-1][1] > snakelist[i][1] and snakelist[i+1][0] > snakelist[i][0]:
                s_corner_rot = pygame.transform.rotate(s_corner_rot,180)
                corner = True
            elif snakelist[i-1][1] < snakelist[i][1] and snakelist[i+1][0] > snakelist[i][0]:
                s_corner_rot = pygame.transform.rotate(s_corner_rot,270)
                corner = True
            elif snakelist[i-1][1] > snakelist[i][1] and snakelist[i+1][0] < snakelist[i][0]:
                s_corner_rot = pygame.transform.rotate(s_corner_rot, 90)
                corner = True
            elif snakelist[i-1][1] < snakelist[i][1] and snakelist[i+1][0] < snakelist[i][0]:
                corner = True
            elif snakelist[i+1][0] - snakelist[i][0] > 0: 
                s_body_rot = pygame.transform.rotate(s_body_rot, 270)
            elif snakelist[i+1][0] - snakelist[i][0] < 0:
                s_body_rot = pygame.transform.rotate(s_body_rot, 90)
            elif snakelist[i+1][1] - snakelist[i][1] > 0:
                s_body_rot = pygame.transform.rotate(s_body_rot, 180)


            if corner is True:
                gameDisplay.blit(s_corner_rot, (snakelist[i][0],snakelist[i][1]))
            else:
                gameDisplay.blit(s_body_rot, (snakelist[i][0],snakelist[i][1]))
            corner = False


        gameDisplay.blit(s_head_rot, (snakelist[-1][0], snakelist[-1][1]))
        gameDisplay.blit(s_tail_rot, (snakelist[0][0], snakelist[0][1]))
        #for XnY in snakelist[:-1]:
    #        pygame.draw.rect(gameDisplay, snake_color, [XnY[0], XnY[1], block_size, block_size])
        

def randappleGen():
    randAppleX = random.randrange(0,display_width-apl_thickness)
    randAppleY = random.randrange(0,display_height-apl_thickness)
    return randAppleX, randAppleY

def text_objects(text,color, size=sfont):
    textSurface = size.render (text, True, color)
    return textSurface, textSurface.get_rect()
    

def message_to_screen(msg, color, y_displace = 0, size=sfont):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)
        
def game_intro():
    intro = True

    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    quit()        
        
        gameDisplay.fill(background)
        
        message_to_screen("___________", snake_color, -160, lfont)
        message_to_screen("| SLITHER |", snake_color, -95, lfont)
        message_to_screen("___________", snake_color, -80, lfont)
        message_to_screen("Eat as many apples as you can, but be careful with biting your tail!", red, 0, sfont)
        message_to_screen("Start game - [ENTER]", white,100, sfont)
        message_to_screen("Exit game - [ESC]/Q", white, 150, sfont)
        pygame.display.update()
        clock.tick(5)

def pause():
    paused = True

    message_to_screen("PAUSED", red, -100, mfont)
    message_to_screen("Continue - [ESC]/C", white, 0, sfont)
    message_to_screen("Exit - Q", white, 50, sfont)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
#        gameDisplay.fill(background)
        clock.tick(5)


def gameLoop():
        block_size = 20
        gameExit = False
        gameOver = False
        lead_x = display_width/2
        lead_y = display_height/2
        lead_x_change = block_size
        lead_y_change = 0
        snakelist = [(0,0),(0,0)]
        snakelen = 5

        FPS = 12
        
        randAppleX, randAppleY = randappleGen()

        while not gameExit:
            if gameOver == True:
                gameDisplay.fill(background)
                message_to_screen("GAME OVER", red, -50, lfont)
                message_to_screen("Play again - [ENTER]", white, 50, sfont)
                message_to_screen("Exit game - [ESC]/Q", white, 100, sfont)
                pygame.display.update()

            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                            gameExit = True
                            gameOver = False
                        if event.key == pygame.K_RETURN:
                            gameLoop()
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False

            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT and snakelist[-1][0] <= snakelist[-2][0]:
                        lead_x_change =-block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_RIGHT and snakelist[-1][0] >= snakelist[-2][0]: 
                        lead_x_change = block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_UP and snakelist[-1][1] <= snakelist[-2][1]:
                        lead_y_change = -block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_DOWN and snakelist[-1][1] >= snakelist[-2][1]:
                        lead_y_change = block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_ESCAPE:
                        pause()
                #if event.type == pygame.KEYUP:
                #   if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #       lead_x_change = 0
                #   if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                #       lead_y_change = 0
            if lead_x >= display_width:
                lead_x = 0
            if lead_y >= display_height:
                lead_y = 0
            if lead_x < 0:
                lead_x = display_width
            if lead_y < 0:
                lead_y = display_height
                    
            lead_x += lead_x_change
            lead_y += lead_y_change

            gameDisplay.fill(background)
        
            #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, apl_thickness, apl_thickness])
            gameDisplay.blit(apl, (randAppleX, randAppleY))
            snakehead = []
            snakehead.append(lead_x)
            snakehead.append(lead_y)
            snakelist.append(snakehead)

            if len(snakelist) > snakelen:
                del snakelist[0]

            for pos in snakelist[:-1]:
                if pos == snakehead:
                    gameOver = True

            snake(snakelist, block_size)
            
            if lead_x+block_size >= randAppleX and lead_x < randAppleX+apl_thickness and lead_y+block_size >= randAppleY and lead_y < randAppleY+apl_thickness:
                randAppleX, RandAppleY = randappleGen()
                snakelen += 1

            message_to_screen("Pause - [ESC]", white, (display_height/2)-25, xsfont)
            score(snakelen-5)
            pygame.display.update()

            clock.tick(FPS)

        pygame.quit()
        quit()
game_intro()
gameLoop()

