""" Game of Life
	in Python.
"""
from cPickle import dump, load
from os.path import abspath, dirname, exists
import pygame
from sys import argv, exit
from time import sleep


class Game(object):
	""" The Game object, representing
		the overall game state.
	"""

	def __init__(self, resolution, font):
		super(Game, self).__init__()
		self.resolution = resolution
		self.font = font
		self.screen = pygame.display.set_mode(resolution)
		pygame.display.set_caption("Game of Life")
		self.paused = True
		self.generation = 0
		self.grid_size = (resolution[0]/10, resolution[1]/10)
		self.grid = []
		for i in range(self.grid_size[0]):
			self.grid.append([])
			for j in range(self.grid_size[1]):
				self.grid[i].append(False)
		self.folderpath = dirname(abspath(__file__))

	def save_state(self, state_num):
		filepath = self.folderpath+"/../saves/gol_"+state_num+".sav"
		fileobj = open(filepath, "wb")
		dump(self.grid, fileobj)
		fileobj.close()
		print("Saved state #"+state_num+"!")

	def load_state(self, state_num):
		filepath = self.folderpath+"/../saves/gol_"+state_num[1]+".sav"
		if exists(filepath):
			fileobj = open(filepath, "rb")
			self.grid = load(fileobj)
			fileobj.close()
			print("Loaded state #"+state_num[1]+"!")
		else:
			print("State #"+state_num[1]+" has not been saved yet!")

	def num_neighbors(self, i, j):
		num = 0
		ineg = self.grid_size[0]-1 if i == 0 else i-1
		ipos = 0 if i == self.grid_size[0]-1 else i+1
		jneg = self.grid_size[1]-1 if j == 0 else j-1
		jpos = 0 if j == self.grid_size[1]-1 else j+1
		for x in [ineg, i, ipos]:
			for y in [jneg, j, jpos]:
				if not (x == i and y == j) and self.grid[x][y]:
					num += 1
		return num

	def update(self):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit()
				if event.key == pygame.K_SPACE:
					self.paused = not self.paused
				if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
								pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
					self.save_state(pygame.key.name(event.key))
				if event.key in [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5,
								pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9]:
					self.load_state(pygame.key.name(event.key))
			if event.type == pygame.MOUSEBUTTONDOWN:
				(x, y) = pygame.mouse.get_pos()
				self.grid[x/10][y/10] = not self.grid[x/10][y/10]

		if not self.paused:
			self.generation += 1
			new_grid = []
			for i in range(self.grid_size[0]):
				new_grid.append([])
				for j in range(self.grid_size[1]):
					new_grid[i].append(False)

			for i in range(self.grid_size[0]):
				for j in range(self.grid_size[1]):
					if self.grid[i][j]:
						n = self.num_neighbors(i, j)
						if n is 2 or n is 3:
							new_grid[i][j] = True
					elif self.num_neighbors(i, j) == 3:
						new_grid[i][j] = True

			del self.grid
			self.grid = new_grid

	def draw(self):
		self.screen.fill((255, 255, 255))
		for i in range(self.grid_size[0]):
			for j in range(self.grid_size[1]):
				if self.grid[i][j]:
					pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((i*10, j*10), (10, 10)))
		for i in range(1, self.grid_size[0]):
			pygame.draw.line(self.screen, (240, 240, 240), (i*10, 0), (i*10, self.resolution[1]))
		for j in range(1, self.grid_size[1]):
			pygame.draw.line(self.screen, (240, 240, 240), (0, j*10), (self.resolution[0], j*10))

		title_label = self.font.render("Conway's Game of Life in Python", 1, (0, 0, 0))
		self.screen.blit(title_label, (16, 0))
		pause_label = self.font.render("Status: "+("Paused" if self.paused else "Running")+" (Press Space)", 1, (0, 0, 0))
		self.screen.blit(pause_label, (16, 16))
		generation_label = self.font.render("Generation "+str(self.generation), 1, (0, 0, 0))
		self.screen.blit(generation_label, (16, 32))
		state_label = self.font.render("Press 1-9 to save up to 10 states, press F1-F9 to load them.", 1, (0, 0, 0))
		self.screen.blit(state_label, (16, 48))


def main(argv):
	pygame.init()
	font = pygame.font.SysFont("monospace", 16)
	screen_size = (1280, 720)
	game_object = Game(screen_size, font)

	while 1:
		game_object.update()
		game_object.draw()
		pygame.display.flip()
		sleep(float(1/60))  #  60 fps


if __name__ == "__main__":
	main(argv)
