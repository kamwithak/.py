import pygame
import sys
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
navy_blue = (0,0,128)
red = (178,34,34)
gray = (205,201,201)

display_width = 800
display_height = 600

clock = pygame.time.Clock()

#bg = pygame.image.load("wallpaper.jpg")
#size = (width, height) = bg.get_size()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("square_game")

block_size = 25
block_movement = 10
FPS = 20

font = pygame.font.SysFont(None,30)

def message_to_screen(msg, color):

	screen_text = font.render(msg, True, color)
	game_display.blit(screen_text, [210, display_height/2]) #210 centers the text, play with this *

def game_loop():

	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = 0
	lead_y_change = 0

	game_exit = False
	game_over = False

	number_generator_x = random.randint(20, display_width-block_size) #800 - 20
	number_generator_y = random.randint(20, display_height-block_size)

	randAppleX = round(number_generator_x/10)*10 #aligning apple and snake using
	randAppleY = round(number_generator_y/10)*10 #formula that rounds to nearest 10th (snake size is divisible by 10)

	while not game_exit: #event loop

		while game_over == True:

			game_display.fill(gray)
			message_to_screen("You lose! Q to exit, or R to restart  :D", red)
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
				elif event.key == pygame.K_RIGHT:
					lead_x_change = block_movement
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					lead_y_change = -block_movement
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					lead_y_change = block_movement
					lead_x_change = 0

				elif event.key == pygame.K_r: #r to restart game
					game_loop()
				elif event.key == pygame.K_q: #q to exit game
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

		if lead_x == randAppleX or lead_y == randAppleY:
			print("yo yo yo")

		#game_display.blit(bg, (0, 0))
		lead_x += lead_x_change
		lead_y += lead_y_change

		game_display.fill(gray)
		pygame.draw.rect(game_display, red, [randAppleX, randAppleY, block_size, block_size]) #apple
		pygame.draw.rect(game_display, navy_blue, [lead_x, lead_y, block_size, block_size]) #snake
		pygame.display.update()

		clock.tick(FPS) #fps

	pygame.quit()
	sys.exit()

if __name__ == "__main__":

	game_loop()


