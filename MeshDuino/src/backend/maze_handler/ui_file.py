'''
User interface file
'''

import pygame
import time

# displays a horizontally-centred message to the screen
def displayMessage(text, colour, screen, size, screen_size, y_pos, screen_update=None):
	# set the font and size of the message
	# use print(pygame.font.get_fonts()) to see available fonts on system
	displayText = pygame.font.SysFont("ubuntu", size)
	# set the text surface
	textSurface = displayText.render(text, True, colour)
	# get the size of the rectangle surrounding the message
	textRect = textSurface.get_rect()
	# center the container
	textRect.center = ((screen_size[0]/2),y_pos)
	# print it to the screen
	screen.blit(textSurface,textRect)
	# if no secified update screen size
	if screen_update is None:
		screen_update = textRect
	# update the screen with the message
	pygame.display.update(screen_update)
	# print(textRect)
	# return textRect

# displays the user selection of the Main Menu
# bg_colour: background colour, a_colout: active colour, na_colour: inactive colour
def displayMenuSelection(screen, screen_size, choice, bg_colour, a_colour, na_colour):
	screen.fill(bg_colour)
	if choice == 0:
		displayMessage("Yet Another Maze", na_colour, screen, 50, screen_size, screen_size[1]//5)
		displayMessage("Start Game", a_colour, screen, 30, screen_size, screen_size[1]*2//5)
		displayMessage("Settings", na_colour, screen, 30, screen_size, screen_size[1]*3//5)
		displayMessage("Exit", na_colour, screen, 30, screen_size, screen_size[1]*4//5)
	elif choice == 1:
		displayMessage("Yet Another Maze", na_colour, screen, 50, screen_size, screen_size[1]//5)
		displayMessage("Start Game", na_colour, screen, 30, screen_size, screen_size[1]*2//5)
		displayMessage("Settings", a_colour, screen, 30, screen_size, screen_size[1]*3//5)
		displayMessage("Exit", na_colour, screen, 30, screen_size, screen_size[1]*4//5)
	elif choice == 2:
		displayMessage("Yet Another Maze", na_colour, screen, 50, screen_size, screen_size[1]//5)
		displayMessage("Start Game", na_colour, screen, 30, screen_size, screen_size[1]*2//5)
		displayMessage("Settings", na_colour, screen, 30, screen_size, screen_size[1]*3//5)
		displayMessage("Exit", a_colour, screen, 30, screen_size, screen_size[1]*4//5)

# display settings options
# takes in additional grid size and side length parameters
def displaySettingsSeleciton(screen, screen_size, choice, bg_colour, a_colour, na_colour, grid_size, side_length, mode_text):
	screen.fill(bg_colour)
	grid_text = "Grid size: " + str(grid_size)
	side_text = "Side length: " + str(side_length)
	# this is the position of the largest rectangle for mode text to update
	mode_text_rect = (176,316,149,34)
	if choice == 0:
		displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
		displayMessage(grid_text, a_colour, screen, 30, screen_size, screen_size[1]*2//6)
		displayMessage(side_text, na_colour, screen, 30, screen_size, screen_size[1]*3//6)
		displayMessage(mode_text, na_colour, screen, 30, screen_size, screen_size[1]*4//6, mode_text_rect)
		displayMessage("Return", na_colour, screen, 30, screen_size, screen_size[1]*5//6)
	elif choice == 1:
		displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
		displayMessage(grid_text, na_colour, screen, 30, screen_size, screen_size[1]*2//6)
		displayMessage(side_text, a_colour, screen, 30, screen_size, screen_size[1]*3//6)
		displayMessage(mode_text, na_colour, screen, 30, screen_size, screen_size[1]*4//6, mode_text_rect)
		displayMessage("Return", na_colour, screen, 30, screen_size, screen_size[1]*5//6)
	elif choice == 2:
		displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
		displayMessage(grid_text, na_colour, screen, 30, screen_size, screen_size[1]*2//6)
		displayMessage(side_text, na_colour, screen, 30, screen_size, screen_size[1]*3//6)
		displayMessage(mode_text, a_colour, screen, 30, screen_size, screen_size[1]*4//6, mode_text_rect)
		displayMessage("Return", na_colour, screen, 30, screen_size, screen_size[1]*5//6)
	elif choice == 3:
		displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
		displayMessage(grid_text, na_colour, screen, 30, screen_size, screen_size[1]*2//6)
		displayMessage(side_text, na_colour, screen, 30, screen_size, screen_size[1]*3//6)
		displayMessage(mode_text, na_colour, screen, 30, screen_size, screen_size[1]*4//6, mode_text_rect)
		displayMessage("Return", a_colour, screen, 30, screen_size, screen_size[1]*5//6)

# settings function - enables user to choose size of the map
def settingsMenu(screen, screen_size, bg_colour, a_colour, na_colour, cooldown, start_timer, g_size, s_length):

	options = {0:"Grid Size", 1:"Side Length", 2:"Return", 3:"Mode"}
	modes = {0:"Solo", 1:"Two Player", 2:"Race", 3:"Chase", 4:"Escape"}
	current_mode = 0
	current_selection = options[0]

	grid_size = g_size
	side_length = s_length

	pygame.display.set_caption("Settings")

	screen.fill(bg_colour)

	pygame.display.flip()

	displaySettingsSeleciton(screen, screen_size, 0, bg_colour, a_colour, na_colour,\
							 grid_size, side_length, modes[current_mode])

	carryOn = True

	while carryOn:
		# action (close screen)
		for event in pygame.event.get():# user did something
			if event.type == pygame.QUIT:
				carryOn = False
				Run = False

		# get pressed keys
		keys = pygame.key.get_pressed()

		# if the cooldown timer is reached
		if (pygame.time.get_ticks() - start_timer > cooldown):
			if current_selection == options[0]:
				# if user pressed down arrow key
				if keys[pygame.K_DOWN]:
					# display selection
					displaySettingsSeleciton(screen, screen_size, 1, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					current_selection = options[1]
					# restart cooldown timer
					start_timer = pygame.time.get_ticks()
				# decrease the grid size by 1
				if keys[pygame.K_LEFT]:
					grid_size -= 1
					if grid_size < 10:
						grid_size = 10
					displaySettingsSeleciton(screen, screen_size, 0, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					start_timer = pygame.time.get_ticks()
				# increase the grid size by 1
				if keys[pygame.K_RIGHT]:
					grid_size += 1
					if grid_size > 35:
						grid_size = 35
					displaySettingsSeleciton(screen, screen_size, 0, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					start_timer = pygame.time.get_ticks()
			elif current_selection == options[1]:
				# if user pressed down arrow key
				if keys[pygame.K_DOWN]:
					# display selection
					displaySettingsSeleciton(screen, screen_size, 2, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					current_selection = options[2]
					# restart cooldown timer
					start_timer = pygame.time.get_ticks()
				# if user pressed up arrow key
				if keys[pygame.K_UP]:
					displaySettingsSeleciton(screen, screen_size, 0, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					current_selection = options[0]
					start_timer = pygame.time.get_ticks()
				# decrease the grid size by 1
				if keys[pygame.K_LEFT]:
					side_length -= 1
					if side_length < 10:
						side_length = 10
					displaySettingsSeleciton(screen, screen_size, 1, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					start_timer = pygame.time.get_ticks()
				# increase the grid size by 1
				if keys[pygame.K_RIGHT]:
					side_length += 1
					if side_length > 15:
						side_length = 15
					displaySettingsSeleciton(screen, screen_size, 1, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					start_timer = pygame.time.get_ticks()
			elif current_selection == options[2]:
				if keys[pygame.K_DOWN]:
					displaySettingsSeleciton(screen, screen_size, 3, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					current_selection = options[3]
					start_timer = pygame.time.get_ticks()
				if keys[pygame.K_UP]:
					displaySettingsSeleciton(screen, screen_size, 1, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					current_selection = options[1]
					start_timer = pygame.time.get_ticks()
				# mode selection
				if keys[pygame.K_LEFT]:
					current_mode -= 1
					if current_mode < 0:
						current_mode = 0
					displaySettingsSeleciton(screen, screen_size, 2, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					start_timer = pygame.time.get_ticks()
				if keys[pygame.K_RIGHT]:
					current_mode += 1
					if current_mode > 4:
						current_mode = 4
					displaySettingsSeleciton(screen, screen_size, 2, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					start_timer = pygame.time.get_ticks()
			elif current_selection == options[3]:
				# if user pressed up arrow key
				if keys[pygame.K_UP]:
					# display selection 1
					displaySettingsSeleciton(screen, screen_size, 2, bg_colour, a_colour, na_colour,\
											 grid_size, side_length, modes[current_mode])
					current_selection = options[2]
					start_timer = pygame.time.get_ticks()
				# press enter key to select this option
				if keys[pygame.K_RETURN]:
					carryOn = False

	# reset the caption
	pygame.display.set_caption("Main Menu")

	# return selected grid size and side length
	return grid_size, side_length, current_mode

# start screen function
def startScreen():
	pygame.init()

	# default maze settings
	grid_size = 20
	side_length = 10

	# Define colours
	BLACK = (0,0,0)
	WHITE = (255,255,255)
	GOLD = (249,166,2)

	screen_size = (500,500)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Main Menu")
	screen.fill(WHITE)

	pygame.display.flip()

	displayMenuSelection(screen, screen_size, 0, WHITE, GOLD, BLACK)

	options = {0:"Start Game", 1:"Settings", 2:"Exit"}
	current_selection = options[0]

	clock = pygame.time.Clock()

	mode = 0

	Run = True

	carryOn = True
	Settings = False

	# set cooldown for key clicks
	cooldown = 150
	# initialize cooldown timer for key clicks
	start_timer = pygame.time.get_ticks()

	while carryOn:
		# action (close screen)
		for event in pygame.event.get():# user did something
			if event.type == pygame.QUIT:
				carryOn = False
				Run = False

		# get pressed keys
		keys = pygame.key.get_pressed()

		# if the cooldown timer is reached
		if (pygame.time.get_ticks() - start_timer > cooldown):
			if current_selection == options[0]:
				# if user pressed down arrow key
				if keys[pygame.K_DOWN]:
					# display selection 1
					displayMenuSelection(screen, screen_size, 1, WHITE, GOLD, BLACK)
					current_selection = options[1]
					# restart cooldown timer
					start_timer = pygame.time.get_ticks()
				# if user selected this option, break out of loop
				if keys[pygame.K_RETURN]:
					carryOn = False
			elif current_selection == options[1]:
				# if user pressed up arrow key
				if keys[pygame.K_UP]:
					# display selection 0
					displayMenuSelection(screen, screen_size, 0, WHITE, GOLD, BLACK)
					current_selection = options[0]
					start_timer = pygame.time.get_ticks()
				# if user pressed down arrow key
				if keys[pygame.K_DOWN]:
					# display selection 2
					displayMenuSelection(screen, screen_size, 2, WHITE, GOLD, BLACK)
					current_selection = options[2]
					start_timer = pygame.time.get_ticks()
				if keys[pygame.K_RETURN]:
					Settings = True
			elif current_selection == options[2]:
				# if user pressed up arrow key
				if keys[pygame.K_UP]:
					# display selection 1
					displayMenuSelection(screen, screen_size, 1, WHITE, GOLD, BLACK)
					current_selection = options[1]
					start_timer = pygame.time.get_ticks()
				# enter key to select this option
				if keys[pygame.K_RETURN]:
					carryOn = False
					Run = False

		# if the settings option was selected
		if Settings:
			grid_size, side_length, mode = settingsMenu(screen, screen_size, WHITE, GOLD, BLACK, cooldown,\
											 	 start_timer, grid_size, side_length)			
			current_selection = options[0]
			displayMenuSelection(screen, screen_size, 0, WHITE, GOLD, BLACK)
			# refresh the screen
			pygame.display.flip()
			# wait quarter of a second
			time.sleep(0.25)
			start_timer = pygame.time.get_ticks()
			Settings = False

		clock.tick(60)

	pygame.quit()

	return Run, grid_size, side_length, mode

# end game screen
def endGame(mode, value):
	pygame.init()

	# Define colours
	BLACK = (0,0,0)
	GRAY = (100,100,100)
	WHITE = (255,255,255)
	GOLD = (249,166,2)
	GREEN = (0,255,0)
	BLUE = (0,0,255)

	screen_size = (500,500)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Game Over")
	screen.fill(WHITE)

	pygame.display.flip()

	if mode == 0:
		text = "Time: " + str(value) + " s"
		displayMessage("Game Over", BLACK, screen, 50, screen_size, screen_size[1]//4)
		displayMessage(text, BLACK, screen, 30, screen_size, screen_size[1]*2//4)
		displayMessage("Press enter to exit to menu.", BLACK, screen, 20, screen_size,screen_size[1]*3//4)
	elif mode == 1:
		text = "Player " + str(value) + " wins!"
		displayMessage("Game Over", BLACK, screen, 50, screen_size, screen_size[1]//4)
		if value == 1:
			displayMessage(text, GREEN, screen, 30, screen_size, screen_size[1]*2//4)
		else:
			displayMessage(text, BLUE, screen, 30, screen_size, screen_size[1]*2//4)
		displayMessage("Press enter to exit to menu.", BLACK, screen, 20, screen_size,screen_size[1]*3//4)
	elif mode == 2 or mode == 3:
		displayMessage("Game Over", BLACK, screen, 50, screen_size, screen_size[1]//4)
		if value == 1:
			text = "You win!"
			displayMessage(text, GOLD, screen, 30, screen_size, screen_size[1]*2//4)
		else:
			text = "The computer wins!"
			displayMessage(text, GRAY, screen, 30, screen_size, screen_size[1]*2//4)
		displayMessage("Press enter to exit to menu.", BLACK, screen, 20, screen_size,screen_size[1]*3//4)
	elif mode == 4:
		displayMessage("Game Over", BLACK, screen, 50, screen_size, screen_size[1]//4)
		if value == 1:
			text = "You escaped!"
			displayMessage(text, GOLD, screen, 30, screen_size, screen_size[1]*2//4)
		else:
			text = "You were caught!"
			displayMessage(text, GRAY, screen, 30, screen_size, screen_size[1]*2//4)
		displayMessage("Press enter to exit to menu.", BLACK, screen, 20, screen_size,screen_size[1]*3//4)


	carryOn = True

	clock = pygame.time.Clock()

	while carryOn:

		# action (close screen)
		for event in pygame.event.get():# user did something
			if event.type == pygame.QUIT:
				carryOn = False

		# get keys pressed
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RETURN]:
			carryOn = False

		clock.tick(60)

	pygame.quit()
