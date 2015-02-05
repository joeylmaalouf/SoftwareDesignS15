"""
Write a function that takes a list of numbers and returns the cumulative sum;
that is, a new list where the ith element is the sum of the first i+1 elements from the original list.
For example, the cumulative sum of [1, 2, 3] is [1, 3, 6].
"""

import sys


def cumulative_sum_concise(lst):
	return [sum(lst[:i+1]) for i in range(len(lst))]


def cumulative_sum_fast(lst):
	sum = 0
	out = []
	for l in lst:
		sum += l
		out.append(sum)
	return out


def main(argv):
	print(cumulative_sum_concise([1, 2, 3, 4, 5]))
	print(cumulative_sum_fast([1, 2, 3, 4, 5]))


if __name__ == "__main__":
	main(sys.argv)
