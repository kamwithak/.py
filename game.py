import pygame, sys

pygame.init()

white = (255,255,255)
black = (0,0,0)
navy_blue = (0,0,128)
red = (178,34,34)
gray = (205,201,201)

lead_x = 400
lead_y = 400

#bg = pygame.image.load("wallpaper.jpg")
#size = (width, height) = bg.get_size()
game_display = pygame.display.set_mode((800,600)) 
pygame.display.set_caption("test_game")

game_exit = False

while not game_exit: #event loop

	for event in pygame.event.get():

		if event.type == pygame.QUIT: #break loop and exit pygame
			game_exit = True

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				lead_x -= 15
			if event.key == pygame.K_RIGHT:
				lead_x += 15
			if event.key == pygame.K_UP:
				lead_y -= 15
			if event.key == pygame.K_DOWN:
				lead_y += 15

		print(event) #print events 

	#game_display.blit(bg, (0, 0))
	game_display.fill(gray)
	pygame.draw.rect(game_display, navy_blue, [lead_x,lead_y,19,19])
	pygame.display.update()

pygame.quit()
sys.exit()
