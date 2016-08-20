import pygame, sys

pygame.init()

white = (255,255,255)
black = (0,0,0)
navy_blue = (0,0,128)
red = (178,34,34)
gray = (205,201,201)

lead_x = 400
lead_y = 400
lead_x_change = 0
lead_y_change = 0

time = pygame.time.Clock()

#bg = pygame.image.load("wallpaper.jpg")
#size = (width, height) = bg.get_size()
game_display = pygame.display.set_mode((1000,800))
pygame.display.set_caption("test_game")

game_exit = False

while not game_exit: #event loop

	for event in pygame.event.get():

		if event.type == pygame.QUIT: #break loop and exit pygame
			game_exit = True

		if event.type == pygame.KEYDOWN: #left, up -> '-' right, bottom -> '+'
			if event.key == pygame.K_LEFT:
				lead_x_change = -15
				lead_y_change = 0
			elif event.key == pygame.K_RIGHT:
				lead_x_change = 15
				lead_y_change = 0
			elif event.key == pygame.K_UP:
				lead_y_change = -15
				lead_x_change = 0
			elif event.key == pygame.K_DOWN:
				lead_y_change = 15
				lead_x_change = 0

			elif event.key == pygame.K_q: #q to exit program
				pygame.quit()
				sys.exit()

		print(event) #print events

#instantaneously stop motion for a frame (hold down effect)

#		if event.type == pygame.KEYUP: 
#			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#				lead_x_change = 0
#			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
#				lead_y_change = 0

	if lead_x > 1000 or lead_x < 0 or lead_y > 800 or lead_y < 0: #boundaries 
		game_exit = True

	#game_display.blit(bg, (0, 0))
	lead_x += lead_x_change
	lead_y += lead_y_change
	game_display.fill(gray)
	pygame.draw.rect(game_display, navy_blue, [lead_x,lead_y,30,30])
	pygame.display.update()

	time.tick(60) #fps

pygame.quit()
sys.exit()
