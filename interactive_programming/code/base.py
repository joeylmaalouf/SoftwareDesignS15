""" To be imported and used in other files.
"""
import cv2
import pygame


class Box(object):
	""" The Box object, from which
		other classes inherit stuff.
	"""

	def __init__(self, size = (40, 20), pos = (0, 0)):
		self.w = size[0]
		self.h = size[1]
		self.x = pos[0]
		self.y = pos[1]

	def __str__(self):
		return str(self.w)+"x"+str(self.h)+" at "+str(self.x)+","+str(self.y)

	def rect(self):
		return pygame.Rect(self.x, self.y, self.w, self.h)

	def size(self):
		return (self.w, self.h)

	def pos(self):
		return (self.x, self.y)

	def center(self):
		return (self.x+self.w/2, self.y+self.h/2)


class Entity(Box):
	""" The Entity object, an extension of
		the Box class that adds movement.
	"""

	def __init__(self, size = (16, 16), pos = (100, 100), speed = (0, 0)):
		super(Entity, self).__init__(size, pos)
		self.vx = speed[0]
		self.vy = speed[1]

	def move_to(self, x, y):
		self.x = x
		self.y = y

	def move_by(self, vx, vy):
		self.x += vx
		self.y += vy


class Level(object):
	""" The Level object, representing,
		the current level's state.
	"""

	def __init__(self, spawn = (100, 100)):
		self.spawn = spawn
		self.blocks = []
		self.enemies = []
		self.goals = []

	def add_piece(self, w, h, x, y):
		self.blocks.append(Box((w, h), (x, y)))

	def add_enemy(self, w, h, x, y, vx, vy):
		self.enemies.append(Entity((w, h), (x, y), (vx, vy)))

	def add_goal(self, w, h, x, y):
		self.goals.append(Box((w, h), (x, y)))


class Camera(object):
	""" The Camera object, representing
		the state of the webcam input.
	"""

	def __init__(self, device_num):
		self.capture = cv2.VideoCapture(device_num)
		self.width = int(self.capture.get(3))
		self.height = int(self.capture.get(4))
		self.face_cascade = cv2.CascadeClassifier("/usr/include/opencv2/data/haarcascades/haarcascade_frontalface_alt.xml")

	def get_face_coords(self):
		ret, frame = self.capture.read()
		return self.face_cascade.detectMultiScale(frame, minSize = (12, 12))

	def get_face(frame, coords, size):
		return frame[coords[1]:coords[1]+size[1], coords[0]:coords[0]+size[0]]
