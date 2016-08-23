import pygame
import sys
import time
import random

pygame.init()

white = (255,255,255)
black = (22,22,22)
navy_blue = (0,0,128)
green = (0,155,0)
red = (178,34,34)
gray = (205,201,201)

display_width = 800
display_height = 600

clock = pygame.time.Clock()

#bg = pygame.image.load("wallpaper.jpg")
#size = (width, height) = bg.get_size()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("snake_game")

block_size = 15
block_movement = 10 #keep block_movement = 10 for grid effect 
FPS = 19

font_center = pygame.font.SysFont(None,30)
font_for_counter = pygame.font.SysFont(None,40)

def counter_displayer(counter):

	counter_text = font_for_counter.render('SCORE: ' + str(counter), True, gray)
	game_display.blit(counter_text, [20, 550])

def snake(block_size, snake_list):

	for XnY in snake_list:
		pygame.draw.rect(game_display, green, [XnY[0], XnY[1], block_size, block_size]) #drawing snake

def message_to_center_of_screen(msg, color):

	screen_text = font_center.render(msg, True, color)
	game_display.blit(screen_text, [220, display_height/2]) #center the text, play with this *

def game_loop():

	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = 0
	lead_y_change = 0
	counter = 0

	game_exit = False
	game_over = False

	snake_list = []
	snake_length = 7

	randAppleX = round(random.randint(60, 500)/10)*10 #formula that rounds to nearest 10th for grid effect
	randAppleY = round(random.randint(60, 500)/10)*10 #generates random coordinate for initial apple 

	while not game_exit: #event loop

		while game_over == True:

			game_display.fill(black)
			message_to_center_of_screen("You lose! Q to exit, or R to restart  :D", red)
			pygame.display.update()

			for event in pygame.event.get():

				if event.type == pygame.QUIT: #break loops and exit pygame
					game_over = False
					game_exit = True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q: #Q
						game_over = False
						game_exit = True
					if event.key == pygame.K_r: #R
						game_loop()

		for event in pygame.event.get():

			if event.type == pygame.QUIT: #break loop and exit pygame
				game_exit = True

			if event.type == pygame.KEYDOWN: #left, up -> '-' right, bottom -> '+'
				if event.key == pygame.K_LEFT:
					lead_x_change = -block_movement
					lead_y_change = 0
				if event.key == pygame.K_RIGHT:
					lead_x_change = block_movement
					lead_y_change = 0
				if event.key == pygame.K_UP:
					lead_y_change = -block_movement
					lead_x_change = 0
				if event.key == pygame.K_DOWN:
					lead_y_change = block_movement
					lead_x_change = 0

				if event.key == pygame.K_r: #r to restart game
					game_loop()
				if event.key == pygame.K_q: #q to exit game
					pygame.quit()
					sys.exit()

			print(event) #print events

	# ~~ instantaneously stop motion for a frame (hold down effect)

	# 		if event.type == pygame.KEYUP: 
	# 			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
	# 				lead_x_change = 0
	# 			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
	# 				lead_y_change = 0

		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0: #boundaries for game screen
			game_over = True

		if lead_x == randAppleX and lead_y == randAppleY:
			randAppleX = round(random.randint(60, 500)/10)*10 #formula that rounds to nearest 10th for grid effect
			randAppleY = round(random.randint(60, 500)/10)*10 #also regenerates coordinates for new apple
			counter += 1 

		#game_display.blit(bg, (0, 0))
		lead_x += lead_x_change
		lead_y += lead_y_change

		game_display.fill(black)
		counter_displayer(counter)
		pygame.draw.rect(game_display, red, [randAppleX, randAppleY, block_size, block_size]) #drawing apple
		snake_head = []
		snake_head.append(lead_x)
		snake_head.append(lead_y)
		snake_list.append(snake_head)

		if len(snake_list) > snake_length: #line-effect for snake, disable condition if confused
			del snake_list[0]

		snake(block_size, snake_list)

		pygame.display.update()

		clock.tick(FPS) #fps

	pygame.quit()
	sys.exit()

if __name__ == "__main__":

	game_loop()

