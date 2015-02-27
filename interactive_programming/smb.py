""" Super Meat Boy in Python
	Joey L. Maalouf
"""
import pygame
import sys
import time


class Box(object):
	""" The Box object, from which
		other classes inherit stuff.
	"""

	def __init__(self, size = (40, 20), pos = (0, 0)):
		self.w = size[0]
		self.h = size[1]
		self.x = pos[0]
		self.y = pos[1]

	def rect(self):
		return pygame.Rect(self.x, self.y, self.w, self.h)

	def size(self):
		return (self.w, self.h)

	def pos(self):
		return (self.x, self.y)


class MeatBoy(Box):
	""" The Player object, representing
		the player's current state.
	"""

	def __init__(self, size = (16, 16), pos = (0, 0), speed = 1):
		super(MeatBoy, self).__init__(size, pos)
		self.speed = speed

	def move_to(self, x, y):
		self.x = x
		self.y = y

	def move_by(self, dx, dy):
		self.x += dx
		self.y += dy


class Level(object):
	""" The Level object, representing,
		the current level's state.
	"""

	def __init__(self):
		self.blocks = []

	def add_piece(self):
		pass


class Game(object):
	""" The Game object, representing
		the overall game state.
	"""

	def __init__(self, resolution):
		super(Game, self).__init__()
		self.resolution = resolution
		self.screen = pygame.display.set_mode(resolution)
		pygame.display.set_caption("Super Meat Boy")

	def update(self, player, level):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				sys.exit()

		state = pygame.key.get_pressed()
		if state[pygame.K_LEFT] or state[pygame.K_a]:
			player.move_by(-player.speed, 0)
		if state[pygame.K_RIGHT] or state[pygame.K_d]:
			player.move_by(player.speed, 0)

	def draw(self, player, level):
		self.screen.fill((0, 0, 0))
		pygame.draw.rect(self.screen, (200, 0, 0), player.rect())
		for block in level.blocks:
			pygame.draw.rect(self.screen, (100, 100, 100), blocks.rect())


def main(argv):
	pygame.init()
	size = (pygame.display.Info().current_w*3/4, pygame.display.Info().current_h*3/4)
	game_object = Game(size)
	player = MeatBoy()
	level1 = Level()
	level1.add_piece()

	while 1:
		game_object.update(player, level1)
		game_object.draw(player, level1)
		pygame.display.flip()
		time.sleep(float(1/60))  # 60 fps


if __name__ == "__main__":
	main(sys.argv)
