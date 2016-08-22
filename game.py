import pygame
import sys
import time

pygame.init()

white = (255,255,255)
black = (0,0,0)
navy_blue = (0,0,128)
red = (178,34,34)
gray = (205,201,201)

game_exit = False

display_width = 800
display_height = 600

lead_x = display_width/2
lead_y = display_height/2

lead_x_change = 0
lead_y_change = 0

clock = pygame.time.Clock()

#bg = pygame.image.load("wallpaper.jpg")
#size = (width, height) = bg.get_size()
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("test_game")

snake_size = 20
block_size_change = snake_size/2
FPS = 30

font = pygame.font.SysFont(None,25)

def message_to_screen(msg,color):
	screen_text = font.render(msg,True,color)
	game_display.blit(screen_text,[display_width/2, display_height/2])


while not game_exit: #event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #break loop and exit pygame
			game_exit = True
		if event.type == pygame.KEYDOWN: #left, up -> '-' right, bottom -> '+'
			if event.key == pygame.K_LEFT:
				lead_x_change = -block_size_change
				lead_y_change = 0
			elif event.key == pygame.K_RIGHT:
				lead_x_change = block_size_change
				lead_y_change = 0
			elif event.key == pygame.K_UP:
				lead_y_change = -block_size_change
				lead_x_change = 0
			elif event.key == pygame.K_DOWN:
				lead_y_change = block_size_change
				lead_x_change = 0

			elif event.key == pygame.K_q: #q to exit program
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
		game_exit = True

	#game_display.blit(bg, (0, 0))
	lead_x += lead_x_change
	lead_y += lead_y_change
	game_display.fill(gray)
	pygame.draw.rect(game_display, navy_blue, [lead_x,lead_y,snake_size,snake_size])
	pygame.display.update()

	clock.tick(FPS) #fps

message_to_screen("You lose! hehe :D", red)
pygame.display.update()
time.sleep(2)
pygame.quit()
sys.exit()
