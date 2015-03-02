""" Game of Life
	in Python.
"""
import pygame
import sys
import time


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
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				if event.key == pygame.K_SPACE:
					self.paused = not self.paused
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
		pause_label = self.font.render(("Paused" if self.paused else "Running")+" (press space)", 1, (0, 0, 0))
		self.screen.blit(pause_label, (16, 16))
		generation_label = self.font.render("Generation "+str(self.generation), 1, (0, 0, 0))
		self.screen.blit(generation_label, (16, 32))


def main(argv):
	pygame.init()
	font = pygame.font.SysFont("monospace", 16)
	screen_size = (1280, 720)
	game_object = Game(screen_size, font)

	while 1:
		game_object.update()
		game_object.draw()
		pygame.display.flip()
		time.sleep(float(1/60))  #  60 fps


if __name__ == "__main__":
	main(sys.argv)
