"""
Joey L. Maalouf
Software Design, Spring 2015
Franklin W. Olin College of Engineering
"""
from math import cos, pi, sin
from PIL import Image
from random import randint


def build_random_function(min_depth, max_depth):
	""" Builds a random function of depth at least min_depth and depth
		at most max_depth (see assignment writeup for definition of depth
		in this context)

		min_depth: the minimum depth of the random function
		max_depth: the maximum depth of the random function
		returns: the randomly generated function
	"""
	return rand_func_helper(None, randint(min_depth, max_depth))


def rand_func_helper(func, depth):
	""" The recursive helper function for the wrapper function above.

		func: the currently composed function
		depth: how many layers we have left
	"""
	# TODO: actually make use of the func variable and nest the functions
	if depth == 0:
		return func
	def f0(x,y):
		return sin(pi*x)+cos(pi*y)
	def f1(x,y):
		return sin(pi*x)-cos(pi*y)
	def f2(x,y):
		return -sin(pi*x)+cos(pi*y)
	def f3(x,y):
		return -sin(pi*x)-cos(pi*y)
	functions = [f0, f1, f2, f3]
	return rand_func_helper(functions[randint(0, 3)], depth-1)


#def evaluate_random_function(f, x, y):
#	""" Evaluate the random function f with inputs x,y
#		Representation of the function f is defined in the assignment writeup
#
#		f: the function to evaluate
#		x: the value of x to be used to evaluate the function
#		y: the value of y to be used to evaluate the function
#		returns: the function value
#
#		>>> evaluate_random_function(["x"],-0.5, 0.75)
#		-0.5
#		>>> evaluate_random_function(["y"],0.1,0.02)
#		0.02
#	"""
#	return {"x":x, "y":y}[f[0]]


def remap_interval(val, iis, iie, ois, oie):
	""" Given an input value in the interval [input_interval_start,
		input_interval_end], return an output value scaled to fall within
		the output interval [output_interval_start, output_interval_end].

		val: the value to remap
		input_interval_start: the start of the interval that contains all
							  possible values for val
		input_interval_end: the end of the interval that contains all possible
							values for val
		output_interval_start: the start of the interval that contains all
							   possible output values
		output_interval_end: the end of the interval that contains all possible
							output values
		returns: the value remapped from the input to the output interval

		>>> remap_interval(0.5, 0, 1, 0, 10)
		5.0
		>>> remap_interval(5, 4, 6, 0, 2)
		1.0
		>>> remap_interval(5, 4, 6, 1, 2)
		1.5
	"""
	return ois+float((oie-ois))/(iie-iis)*(val-iis)


def color_map(val):
	""" Maps input value between -1 and 1 to an integer 0-255, suitable for
		use as an RGB color code.

		val: value to remap, must be a float in the interval [-1, 1]
		returns: integer in the interval [0,255]

		>>> color_map(-1.0)
		0
		>>> color_map(1.0)
		255
		>>> color_map(0.0)
		127
		>>> color_map(0.5)
		191
	"""
	# NOTE: This relies on remap_interval, which you must provide
	color_code = remap_interval(val, -1, 1, 0, 255)
	return int(color_code)


def test_image(filename, x_size=350, y_size=350):
	""" Generate test image with random pixels and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (randint(0, 255),  # R
							randint(0, 255),  # G
							randint(0, 255))  # B
	im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
	""" Generate computational art and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	red_function = build_random_function(7, 9)
	green_function = build_random_function(7, 9)
	blue_function = build_random_function(7, 9)

	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (
					color_map(red_function(x, y)),
					color_map(green_function(x, y)),
					color_map(blue_function(x, y)))

	im.save(filename)


if __name__ == '__main__':
	import doctest
	doctest.testmod()
	generate_art("computer_generated_art.png")
