""" SkyRoads
	in Python.
"""
from base import Camera
import cv2
import pygame
import sys
import time


class Game(object):
	""" The Game object, representing
		the overall game state.
	"""

	def __init__(self, resolution, camera):
		super(Game, self).__init__()
		self.resolution = resolution
		self.screen = pygame.display.set_mode(resolution)
		pygame.display.set_caption("SkyRoads")
		self.camera = camera

	def update(self):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				self.camera.capture.release()
				cv2.destroyAllWindows()
				sys.exit()

		faces = self.camera.get_face_coords()
		if len(faces) < 1:
			self.current_move = "stay"
		else:
			face = faces[0]
			face_center_x = face[0]+face[2]/2
			if face_center_x < 2*self.camera.width/5:
				self.current_move = "left"
			elif face_center_x > 3*self.camera.width/5:
				self.current_move = "right"
			else:
				self.current_move = "stay"


	def draw(self):
		self.screen.fill((0, 0, 0))
		print(self.current_move)


def main(argv):
	pygame.init()
	screen_size = (1280, 720)
	camera = Camera(0)
	game_object = Game(screen_size, camera)

	while 1:
		game_object.update()
		game_object.draw()
		pygame.display.flip()
		time.sleep(float(1/60))  #  60 fps


if __name__ == "__main__":
	main(sys.argv)
