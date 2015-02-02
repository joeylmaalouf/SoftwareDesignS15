"""
Write a function that takes a list of numbers and returns the cumulative sum;
that is, a new list where the ith element is the sum of the first i+1 elements from the original list.
For example, the cumulative sum of [1, 2, 3] is [1, 3, 6].
"""

import sys


def cumulative_sum(lst):
	return [sum(lst[:i+1]) for i in range(len(lst))]


def main(argv):
	print(cumulative_sum([1, 2, 3, 4]))


if __name__ == "__main__":
	main(sys.argv)
