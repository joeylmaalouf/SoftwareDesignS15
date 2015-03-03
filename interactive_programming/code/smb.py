""" Super Meat Boy
	in Python.
"""
from base import Camera, Entity, Level
import cv2
import pygame
import sys
import time


class MeatBoy(Entity):
	""" The Player object, representing
		the player's current state.
	"""

	def __init__(self, size = (20, 20), pos = (100, 100), speed = (0, 0)):
		super(MeatBoy, self).__init__(size, pos)
		self.vx = speed[0]
		self.vy = speed[1]
		self.grounded = False
		self.alive = True
		self.deaths = 0
		self.won = False


class Game(object):
	""" The Game object, representing
		the overall game state.
	"""

	def __init__(self, resolution, camera, font):
		super(Game, self).__init__()
		self.resolution = resolution
		self.camera = camera
		self.font = font
		self.screen = pygame.display.set_mode(resolution)
		pygame.display.set_caption("Super Meat Boy")


	def close(self):
		self.camera.capture.release()
		cv2.destroyAllWindows()
		sys.exit()


	def update(self, player, level):
		if not player.alive:
			player.deaths += 1
			player.move_to(level.spawn[0], level.spawn[1])
			player.alive = True

		state = pygame.key.get_pressed()
		if state[pygame.K_a]:
			player.vx = -1
		if state[pygame.K_d]:
			player.vx = 1
		if not (state[pygame.K_a] or state[pygame.K_d]):
			player.vx = 0

		player.vy = min(4, player.vy+0.05)
		if player.grounded:
			player.vy = 0

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				self.close()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.close()
				if player.grounded and event.key == pygame.K_w:
					player.vy -= 4

		player.move_by(player.vx, player.vy)

		for block in level.blocks:
			if player.rect().colliderect(block):
				player.grounded = True
				break
			player.grounded = False

		if not player.rect().colliderect(self.screen.get_rect()):
			player.alive = False

		for enemy in level.enemies:
			if player.rect().colliderect(enemy):
				player.alive = False
			enemy.move_by(enemy.vx, enemy.vy)
			if enemy.y+enemy.h/2 > self.resolution[1]:
				enemy.y = enemy.h/2
			elif enemy.y+enemy.h/2 < 0:
				enemy.y = self.resolution[1]-enemy.h/2

		for goal in level.goals:
			if player.rect().colliderect(goal):
				player.won = True

	def draw(self, player, level):
		if player.won:
			win_label = self.font.render("You win!", 1, (255, 255, 0))
			self.screen.blit(win_label, (620, 320))
			pygame.display.flip()
			time.sleep(2)
			sys.exit()
		else:
			self.screen.fill((0, 0, 0))
			pygame.draw.rect(self.screen, (200, 0, 0), player.rect())
			for block in level.blocks:
				pygame.draw.rect(self.screen, (128, 128, 128), block.rect())
			for enemy in level.enemies:
				pygame.draw.rect(self.screen, (255, 128, 0), enemy.rect())
			for goal in level.goals:
				pygame.draw.rect(self.screen, (0, 255, 0), goal.rect())
			control_label = self.font.render("Use WASD to move. Avoid the enemies and make it to the goal!", 1, (255, 255, 255))
			self.screen.blit(control_label, (16, 16))
			death_label = self.font.render(str(player.deaths)+(" Death" if player.deaths == 1 else " Deaths"), 1, (0, 255, 255))
			self.screen.blit(death_label, (16, 684))


def main(argv):
	pygame.init()
	size = (1280, 720)
	camera = Camera(0)
	font = pygame.font.SysFont("monospace", 16)
	game_object = Game(size, camera, font)
	level1 = Level()
	player = MeatBoy(pos = level1.spawn)
	level1.add_piece(128, 12, 8, 400)
	level1.add_piece(64, 10, 180, 480)
	level1.add_piece(80, 8, 300, 550)
	level1.add_enemy(24, 24, 430, 8, 0, 1)
	level1.add_enemy(24, 24, 430, 360, 0, 1)
	level1.add_piece(80, 12, 500, 500)
	level1.add_piece(96, 16, 640, 600)
	level1.add_piece(64, 16, 800, 560)
	level1.add_enemy(32, 32, 900, 8, 0, -1.5)
	level1.add_enemy(32, 32, 900, 360, 0, -1.5)
	level1.add_goal(64, 64, 1000, 500)

	while 1:
		game_object.update(player, level1)
		game_object.draw(player, level1)
		pygame.display.flip()
		time.sleep(float(1/60))  #  60 fps


if __name__ == "__main__":
	main(sys.argv)
