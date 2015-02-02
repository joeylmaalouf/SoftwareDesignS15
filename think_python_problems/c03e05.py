"""
1. Write a function that draws a grid like the following:
+ - - - - + - - - - +
|         |         |
|         |         |
|         |         |
|         |         |
+ - - - - + - - - - +
|         |         |
|         |         |
|         |         |
|         |         |
+ - - - - + - - - - +
Hint: to print more than one value on a line, you can print a comma-separated sequence:
print '+', '-'
If the sequence ends with a comma, Python leaves the line unfinished,
so the value printed next appears on the same line.
print '+', 
print '-'
The output of these statements is '+ -'.
A print statement all by itself ends the current line and goes to the next line.
2. Write a function that draws a similar grid with four rows and four columns.
"""

import sys


def draw_grid(size):
	hb = "+" + (size * " - - - - +")
	print(hb)
	for i in range(size):
		vb = "|" + (size * "         |")
		for j in range(4):
			print(vb)
		print(hb)


def main(argv):
	draw_grid(2)
	draw_grid(3)
	draw_grid(4)
	draw_grid(10)


if __name__ == "__main__":
	main(sys.argv)
