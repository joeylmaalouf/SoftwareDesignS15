"""
Write a compare function that returns
 1 if x >  y
 0 if x == y
-1 if x <  y
"""

import sys


def compare(x, y):
	return 0 if x == y else (1 if x > y else -1)


def main(argv):
	print(compare(1, 0))
	print(compare(0, 0))
	print(compare(0, 1))


if __name__ == "__main__":
    main(sys.argv)
