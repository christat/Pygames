import pygame
import numpy

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

def Main():
	pygame.init()
	clk = pygame.time.Clock()
	FPS = 60
	
	
	
	#AREAS
	screen_width, screen_height = 800, 600
	screen = pygame.display.set_mode((screen_width,screen_height))
#	canvas - pygame.surface.Surface((screen_width,screen_height))
	paddle_width = 15
	paddle_height = screen_height/6
	radius = 10

	#POSITIONS
	player_pos_x, ai_pos_x = paddle_width, screen_width-(2*paddle_width)
	player_pos_y = ai_pos_y = int((screen_height/2) - (paddle_height/2))
	ball_pos_x = ball_pos_y = int(screen_width/2)

	#MOVEMENT RATES
	mv_player =  mv_ai = 0
	mv_rate, ai_rate, ball_rate_x, ball_rate_y = 20, 20, 6, 2 
	ball_vector = numpy.array([ball_rate_x,ball_rate_y])
	

	pygame.draw.rect(screen, white, (player_pos_x, player_pos_y, paddle_width, paddle_height) )
	pygame.draw.rect(screen, white, (ai_pos_x, ai_pos_y, paddle_width, paddle_height) )
	pygame.draw.circle(screen, red, (ball_pos_x, ball_pos_y), radius )

	#INPUT HANDLING
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				if event.key == pygame.K_UP:
					mv_player = -mv_rate
				if event.key == pygame.K_DOWN:
					mv_player = mv_rate	
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					mv_player = 0
		
		#PADDLES' BARRIERS
		if player_pos_y < 0:
			player_pos_y = 0 
		elif player_pos_y + paddle_height >= screen_height:
			player_pos_y = screen_height - paddle_height

		if ai_pos_y < 0:
			ai_pos_y = 0
		elif ai_pos_y + paddle_height >= screen_height:
			ai_pos_y = screen_height - paddle_height		

		#BALL COLLISION FOR BOUNDARIES
		if ball_pos_y-radius <= 0:
			ball_vector[1]=ball_rate_y
		elif ball_pos_y+radius >= screen_height:
			ball_vector[1]=-ball_rate_y

		#BALL COLLISION FOR AI
		if ball_pos_x > screen_width-(3*paddle_width) and ball_pos_x < screen_width-paddle_width:
			if ball_pos_x + radius >= ai_pos_x:
				if ball_pos_y+radius >= ai_pos_y and ball_pos_y-radius <= ai_pos_y+paddle_height:
					ball_vector[0]=-ball_rate_x

		#BALL COLLISION FOR PLAYER
		elif ball_pos_x < 3*paddle_width and ball_pos_x > paddle_width:
			if ball_pos_x - radius <= player_pos_x+paddle_width:
				if ball_pos_y+radius >= player_pos_y and ball_pos_y-radius <= player_pos_y+paddle_height:
					ball_vector[0]=ball_rate_x

		#*VERY* LIMITED AI
		if ball_pos_x > screen_width/2  and ball_pos_x < screen_width:
			if ball_pos_y - radius > ai_pos_y+paddle_height:
				mv_ai = ai_rate
			elif ball_pos_y + radius < ai_pos_y:
				mv_ai = -ai_rate
			else:
				mv_ai = 0 

		#UPDATE POSITIONS
		player_pos_y += mv_player
		ai_pos_y += mv_ai
		ball_pos_x += ball_vector[0]
		ball_pos_y += ball_vector[1]

		#SCORE HANDLING


		#GRAPHICS UPDATE
		screen.fill(black)
		pygame.draw.rect(screen, white, (player_pos_x, player_pos_y, paddle_width, paddle_height) )
		pygame.draw.rect(screen, white, (ai_pos_x, ai_pos_y, paddle_width, paddle_height) )
		pygame.draw.circle(screen, red, (ball_pos_x, ball_pos_y), radius )
		
		pygame.display.update()
		clk.tick(FPS)

	pygame.quit()
	quit()	


if __name__ == '__main__':
	Main()
