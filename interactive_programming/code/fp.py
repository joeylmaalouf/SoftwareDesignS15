""" Floating Point
	in Python.
"""
from base import Entity, Level
import pygame
import sys
import time


class Player(Entity):
	""" The Player object, representing
		the player's current state.
	"""

	def __init__(self, size = (20, 20), pos = (100, 100), speed = (0, 0)):
		super(Player, self).__init__(size, pos)
		self.vx = speed[0]
		self.vy = speed[1]
		self.grappling = False
		self.grapple_point = (0, 0)


class Game(object):
	""" The Game object, representing
		the overall game state.
	"""

	def __init__(self, resolution):
		super(Game, self).__init__()
		self.resolution = resolution
		self.screen = pygame.display.set_mode(resolution)
		pygame.display.set_caption("Floating Point")

	def update(self, player, level):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				player.grapple_point = pygame.mouse.get_pos()
				player.grappling = True
			if event.type == pygame.MOUSEBUTTONUP:
				player.grappling = False

	def draw(self, player, level):
		self.screen.fill((0, 0, 0))
		pygame.draw.rect(self.screen, (200, 0, 0), player.rect())
		for block in level.blocks:
			pygame.draw.rect(self.screen, (128, 128, 128), block.rect())
		for enemy in level.enemies:
			pygame.draw.rect(self.screen, (255, 128, 0), enemy.rect())
		for goal in level.goals:
			pygame.draw.rect(self.screen, (0, 255, 0), goal.rect())
		if player.grappling:
			pygame.draw.line(self.screen, (255, 0, 0), player.center(), player.grapple_point)


def main(argv):
	pygame.init()
	size = (1280, 720)
	game_object = Game(size)
	level1 = Level()
	player = Player(pos = level1.spawn)
	level1.add_piece(128, 12, 8, 400)

	while 1:
		game_object.update(player, level1)
		game_object.draw(player, level1)
		pygame.display.flip()
		time.sleep(float(1/60))  #  60 fps


if __name__ == "__main__":
	main(sys.argv)
