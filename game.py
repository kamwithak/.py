import pygame
import sys
import time
import random

pygame.init()

white = (255,255,255)
bright_blue = (63,192,255)
black = (22,22,22)
navy_blue = (0,0,128)
green = (0,155,0)
red = (178,34,34)
gray = (205,201,201)

display_width = 800
display_height = 600

clock = pygame.time.Clock()

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("snake_game")
img = pygame.image.load("snake_head.jpg")

block_size = 20 #used for snake size
apple_thickness = 22 #used for apple size
block_movement = 10 #snake movement
FPS = 30 #frames per second
#direction = "left" #initial direction for head of snake

small_font = pygame.font.SysFont("comicsansms", 25)
medium_font = pygame.font.SysFont("comicsansms", 35)
large_font = pygame.font.SysFont("comicsansms", 45)

def ingame_counter_displayer(counter):

	ingame_counter_text = small_font.render('SCORE: ' + str(counter), True, white)
	game_display.blit(ingame_counter_text, [20, 550])

def final_counter_displayer(counter):

	final_counter_text = small_font.render('FINAL SCORE: ' + str(counter), True, white)
	game_display.blit(final_counter_text, [20, 550])

def snake(block_size, snake_list):

	# if direction == "up":
	# 	head = img
	# if direction == "down":
	# 	head = pygame.transform.rotate(img, 180)
	# if direction == "right":
	# 	head = pygame.transform.rotate(img, 270)
	# if direction == "left":
	# 	head = pygame.transform.rotate(img, 90)

	for XnY in snake_list: #uncomment direction code -> snake_list[:-1] on current line
		pygame.draw.rect(game_display, green, [XnY[0], XnY[1], block_size, block_size]) #drawing snake

	#game_display.blit(head, (snake_list[-1][0], snake_list[-1][1]))

def text_objects(text, color, size):

	if size == "small":
		text_surface = small_font.render(text, True, color)
	elif size == "medium":
		text_surface = medium_font.render(text, True, color)
	elif size == "large":
		text_surface = large_font.render(text, True, color)

	return text_surface, text_surface.get_rect()
	
def message_to_center(msg, color, y_displace=0, size="small"):

	text_surf, text_rect = text_objects(msg, color, size)
	text_rect.center = (display_width/2), (display_height/2) + y_displace
	game_display.blit(text_surf, text_rect)

def game_loop():

	#global direction
	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = -10
	lead_y_change = 0
	counter = 0

	game_exit = False
	game_over = False
	game_success = False

	snake_list = []
	snake_length = 0 #init snake length

	randAppleX = round(random.randint(60, 500))#/10)*10 #formula that rounds to nearest 10th for grid effect (currently commented)
	randAppleY = round(random.randint(60, 500))#/10)*10 #generates random coordinate for initial apple 

	while not game_exit: #event loop

		while game_over == True:

			game_display.fill(black)
			message_to_center("Game over!", red, -60, "large")
			message_to_center("Press Q to exit, or R to restart  :D", white, 0, "medium")
			final_counter_displayer(counter)
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

		while game_success == True:

			game_display.fill(black)
			message_to_center("Successfully Completed!", green, -63, "large")
			message_to_center("Press Q to exit, or R to restart  :D", white, 0, "medium")
			final_counter_displayer(counter)
			pygame.display.update()

			for event in pygame.event.get():

				if event.type == pygame.QUIT: #break loops and exit pygame
					game_success = False
					game_exit = True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q: #Q
						game_success = False
						game_exit = True
					if event.key == pygame.K_r: #R
						game_loop()

		for event in pygame.event.get():

			if event.type == pygame.QUIT: #break loop and exit pygame
				game_exit = True

			if event.type == pygame.KEYDOWN: #left, up -> '-' right, bottom -> '+'
				if event.key == pygame.K_LEFT:
					direction = "left"
					lead_x_change = -block_movement
					lead_y_change = 0
				if event.key == pygame.K_RIGHT:
					direction = "right"
					lead_x_change = block_movement
					lead_y_change = 0
				if event.key == pygame.K_UP:
					direction = "up"
					lead_y_change = -block_movement
					lead_x_change = 0
				if event.key == pygame.K_DOWN:
					direction = "down"
					lead_y_change = block_movement
					lead_x_change = 0

				if event.key == pygame.K_r: #r to restart game
					game_loop()
				if event.key == pygame.K_q: #q to exit game
					pygame.quit()
					sys.exit()

			print(event) #print events

	# ~~ (hold down effect)

	# 		if event.type == pygame.KEYUP: 
	# 			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
	# 				lead_x_change = 0
	# 			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
	# 				lead_y_change = 0

		# ~~ snake and apple meet 

		# if lead_x >= randAppleX and lead_x <= randAppleX + apple_thickness:
		# 	if lead_y >= randAppleY and lead_y <= randAppleY + apple_thickness:
		# 		randAppleX = round(random.randint(60, 500))#/10)*10 #formula that rounds to nearest 10th for grid effect (currently commented)
		# 		randAppleY = round(random.randint(60, 500))#/10)*10 #also regenerates coordinates for new apple
		# 		snake_length += 1 #increase snake length
		# 		counter += 1 #adjust score 

		#game_display.blit(bg, (0, 0))
		lead_x += lead_x_change
		lead_y += lead_y_change

		snake_head = []
		snake_head.append(lead_x)
		snake_head.append(lead_y)
		snake_list.append(snake_head)

		game_display.fill(black)
		pygame.draw.rect(game_display, red, [randAppleX, randAppleY, apple_thickness, apple_thickness]) #drawing apple
		snake(block_size, snake_list)
		ingame_counter_displayer(counter)

		if len(snake_list) > snake_length: #line-effect for snake, disable condition if confused
			del snake_list[0]

		for each_segment in snake_list[:-1]: #head of snake meets body of snake = game over
			if each_segment == snake_head:
				game_over = True

		if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness:
			if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness:
		 		randAppleX = round(random.randint(60, 500))#/10)*10 #formula that rounds to nearest 10th for grid effect (currently commented)
		 		randAppleY = round(random.randint(60, 500))#/10)*10 #regenerates coordinates for new apple
		 		snake_length += 5 #increases snake length
		 		counter += 1 #adjusts score

		if counter == 20:
			game_success = True

		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0: #boundaries for game screen
			game_over = True

		clock.tick(FPS) #fps
		pygame.display.update()


	pygame.quit()
	sys.exit()

if __name__ == "__main__":

	game_loop()
