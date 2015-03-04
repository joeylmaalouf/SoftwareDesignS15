from PIL import Image, ImageDraw
from random import randint
from sys import argv
""" approximate images using genalg to optimize ovals
https://www.youtube.com/watch?v=rGt3iMAJVT8
https://www.youtube.com/watch?v=dO05XcXLxGs
-python imaging library (PIL)?
-evaluate how close each pixel value is in the two images, the one we're trying to mimic and our representation
-make gif of best image each generation?
-maybe use hill climbing? only actually mutate an individual if the new fitness is an improvement;
	this could mean that I could attempt mutation on every individual
	(which is rather greedy, so I should still scramble a few for the sake of eventually getting
	out of local maxima, rather than global, but is that even an issue with image approximation?)
"""


def random_ellipse(resolution):
			return [randint(0, resolution[0]-1), randint(0, resolution[1]-1),          #  xcoord, ycoord,
					randint(1, (resolution[0]-1)/2), randint(1, (resolution[1]-1)/2),  #  xradius, yradius,
					randint(0, 255)]                                                   #  brightness


class Individual(object):
	def __init__(self, resolution):
		self.numovals = 200
		self.numchros = self.numovals*5
		self.solution = []
		for i in range(self.numovals):
			self.solution.extend(random_ellipse(resolution))
		self.fitness = 0

	def make_image(self, resolution):
		self.image = Image.new("RGB", resolution)
		draw = ImageDraw.Draw(self.image)
		for i in range(self.numovals):
			bounds = (self.solution[5*i]-self.solution[5*i+2], self.solution[5*i+1]-self.solution[5*i+3],
					  self.solution[5*i]+self.solution[5*i+2], self.solution[5*i+1]+self.solution[5*i+3])
			draw.ellipse(bounds, fill = self.solution[5*i+4])

	def mutate(self):
		pass

	def scramble(self):
		for i in range(self.numchros):
			self.mutate()

	def payoff(self, resolution, goal_access):
		diff = 0
		self_access = self.image.load()
		for i in range(resolution[0]):
			for j in range(resolution[1]):
				diff += abs(self_access[i, j][0]-goal_access[i, j])
		self.fitness = diff


def main(argv):
	goal_image = Image.open("goal.jpg").convert("L")
	goal_access = goal_image.load()
	resolution = goal_image.size
	popsize = 100
	population = [Individual(resolution) for i in range(popsize)]
	generation = 0
	while(True):
		for individual in population:
			individual.make_image(resolution)
			individual.payoff(resolution, goal_access)


if __name__ == "__main__":
	main(argv)
