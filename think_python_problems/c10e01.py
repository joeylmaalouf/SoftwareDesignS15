"""
Write a function called nested_sum that takes
a nested list of integers and add up the elements
from all of the nested lists.
"""

import sys


def nested_sum(lst):
	return sum(item for sublist in lst for item in sublist)


def main(argv):
	print(nested_sum([[1, 2, 3, 4], [5, 6]]))


if __name__ == "__main__":
	main(sys.argv)
