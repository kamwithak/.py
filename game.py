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
game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption("test_game")

game_exit = False

while not game_exit: #event loop

	for event in pygame.event.get():

		if event.type == pygame.QUIT: #break loop and exit pygame
			game_exit = True

		if event.type == pygame.KEYDOWN: # left, up -> '-' right, bottom -> '+'
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				lead_x_change = -15
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				lead_x_change = 15
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				lead_y_change = -15
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				lead_y_change = 15

		print(event) #print events

	#game_display.blit(bg, (0, 0))
	lead_x += lead_x_change
	lead_y += lead_y_change
	game_display.fill(gray)
	pygame.draw.rect(game_display, navy_blue, [lead_x,lead_y,20,20])
	pygame.display.update()

	time.tick(29) #fps

pygame.quit()
sys.exit()
