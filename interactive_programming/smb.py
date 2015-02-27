""" Super Meat Boy in Python
	Joey L. Maalouf

	NOTE TO SELF: ADD VELOCITY AND ACCLERATION TO PLAYER, LIKE IN SMASH 5
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

	def __init__(self, size = (16, 16), pos = (100, 100), speed = (0, 0)):
		super(MeatBoy, self).__init__(size, pos)
		self.vx = speed[0]
		self.vy = speed[1]
		self.grounded = False
		self.alive = True

	def move_to(self, x, y):
		self.x = x
		self.y = y

	def move_by(self, vx, vy):
		self.x += vx
		self.y += vy

	def tangent_to(self, block):
		pass


class Level(object):
	""" The Level object, representing,
		the current level's state.
	"""

	def __init__(self):
		self.blocks = []

	def add_piece(self, w, h, x, y):
		self.blocks.append(Box((w, h), (x, y)))


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
			if (event.type == pygame.QUIT):
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				if player.grounded and event.key == pygame.K_SPACE:
					player.vy = -4

		player.vy += .05
		state = pygame.key.get_pressed()
		if state[pygame.K_a]:
			player.vx = -1
		if state[pygame.K_d]:
			player.vx = 1
		if not (state[pygame.K_a] or state[pygame.K_d]):
			player.vx = 0

		player.move_by(player.vx, player.vy)

		for block in level.blocks:
			if player.tangent_to(block):
				player.grounded = True
				break
			player.grounded = False

		if not player.rect().colliderect(self.screen.get_rect()):
			player.alive = False

	def draw(self, player, level):
		self.screen.fill((0, 0, 0))
		pygame.draw.rect(self.screen, (200, 0, 0), player.rect())
		for block in level.blocks:
			pygame.draw.rect(self.screen, (128, 128, 128), block.rect())


def main(argv):
	pygame.init()
	size = (1280, 720)
	game_object = Game(size)
	player = MeatBoy()
	level1 = Level()
	#  level1.add_piece(1280, 4, 0, 716)
	level1.add_piece(128, 12, 8, 400)
	level1.add_piece(48, 24, 200, 500)
	level1.add_piece(48, 24, 300, 550)

	while 1:
		game_object.update(player, level1)
		game_object.draw(player, level1)
		pygame.display.flip()
		time.sleep(float(1/60))  # 60 fps


if __name__ == "__main__":
	main(sys.argv)
