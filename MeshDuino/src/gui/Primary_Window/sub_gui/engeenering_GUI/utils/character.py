'''
Character class
'''

import pygame
from time import sleep

class Character:
	# escape is a boolean for "escape mode", keys is a list of tuples (coordinates)
	def __init__(self, screen, side_length, border_width, valid_points, start_point, end_point, current_position, a_colour, na_colour,\
				 escape=False, keys=None, k_colour=None):

		self.screen = screen # pygame screen
		self.side_length = side_length # length of the grid unit
		self.border_width = border_width # border width of the grid unit
		self.start_point = start_point # starting point of character in maze stored as a tuple
		self.end_point = end_point # end point of character in maze (tuple)
		self.current_position = current_position # current position of character (tuple)
		self.a_colour = a_colour # active colour of the character (tuple of 3 elements) RGB colour
		self.na_colour = na_colour # inactive colour of the character (tuple of 3 elements) RGB colour
		# below are initializations for escape mode
		self.escape = escape
		self.keys = keys
		self.k_colour = k_colour
		self.unlocked = False
		self.wallBreaks = 1
		self.increaseCompSpeed = False
			
		# draw the initial position of the character
		self.draw_position()

	# draw the character
	def draw_position(self):
		pygame.draw.rect(self.screen, self.a_colour, [self.border_width+(self.side_length+self.border_width)*self.current_position[0],\
			self.border_width+(self.side_length+self.border_width)*self.current_position[1], self.side_length, self.side_length])

	# move the character to next position
	def move_character(self, next_position):
		# create a rectangle for the current position
		current_rect = [self.border_width+(self.side_length+self.border_width)*self.current_position[0],\
						self.border_width+(self.side_length+self.border_width)*self.current_position[1],\
						self.side_length, self.side_length]
		# create a rectangle for the next position
		next_rect = [self.border_width+(self.side_length+self.border_width)*next_position[0],\
					 self.border_width+(self.side_length+self.border_width)*next_position[1],\
					 self.side_length, self.side_length]
		# draw the previous position of the character as an inactive block
		pygame.draw.rect(self.screen, self.na_colour, current_rect)
		# update the screen at the current point
		pygame.display.update(current_rect)
		# draw the next position of the character
		pygame.draw.rect(self.screen, self.a_colour, next_rect)
		# update the screen at the next point
		pygame.display.update(next_rect)
		# update the current position of the character to the next position
		self.current_position = next_position

		# if it is escape mode then check if on key
		if self.escape is True:
			# remove the key if the player is at the key position
			if self.current_position in self.keys:
				self.keys.remove(self.current_position)
				# add a bonus wall break every two keys
				if len(self.keys)%2 == 0:
					self.wallBreaks += 1
					self.increaseCompSpeed = True

	# draw the intermediate steps when moving a character
	def move_character_smooth(self, next_position, steps):
		# go right
		if next_position[0] != self.current_position[0]:
			# from i = 1 to steps
			for i in range(1,steps+1):
				# short delay between each intermediate step
				sleep(0.005)
				difference = (next_position[0]-self.current_position[0])*i/steps
				next_pos = (self.current_position[0]+difference, self.current_position[1])
				self.move_character(next_pos)
		else:
			for i in range(1,steps+1):
				sleep(0.005)
				difference = (next_position[1]-self.current_position[1])*i/steps
				next_pos = (self.current_position[0], self.current_position[1]+difference)
				self.move_character(next_pos)

	# return the current position of the character
	def get_current_position(self):
		return self.current_position

	# end goal flag
	def reached_goal(self):
		if self.current_position == self.end_point:
			return True
		else:
			return False

	# ---------- Escape mode functions ---------- #

	# get wallBreaks
	def get_wallBreaks(self):
		return self.wallBreaks

	# use wallBreak
	def use_wallBreak(self):
		self.wallBreaks -= 1

	# get keys left
	def get_keys_left(self):
		if self.keys:
			return len(self.keys)
		else:
			return 0

	# draw keys
	def draw_keys(self):
		for key in self.keys:
			pygame.draw.rect(self.screen, self.k_colour, [self.border_width+(self.side_length+self.border_width)*key[0],\
							 self.border_width+(self.side_length+self.border_width)*key[1], self.side_length, self.side_length])

	# increase the computer speed flag
	def increase_computer_speed(self):
		if self.increaseCompSpeed:
			self.increaseCompSpeed = False
			return True
		else:
			return False

	# collected all keys flag
	def collected_all(self):
		# if the keys list is empty, it means that all of the keys were collected
		if not self.keys:
			self.unlocked = True
			return True
		else:
			return False

	# escaped goal flag
	def escaped(self):
		if self.unlocked is True and self.reached_goal():
			return True
		else:
			return False