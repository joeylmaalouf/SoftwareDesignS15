import doctest
import sys


def wc(text):
	"""
	>>> wc("Hello world!")
	12 characters
	10 letters and numbers
	2 words
	"""
	print(str(len(text))+" characters")
	print(str(len([c for c in text if c.isalnum()]))+" letters and numbers")
	print(str(len(text.split()))+" words")


def main(argv):
	doctest.testmod()
	wc("Hello world! This is the sample text.")


if __name__ == "__main__":
	main(sys.argv)
