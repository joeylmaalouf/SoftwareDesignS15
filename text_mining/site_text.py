from pattern.web import URL, plaintext
from sys import argv


def main(argv):
	print(plaintext(URL(argv[1]).download(), linebreaks = 1, indentation = False))


if __name__ == "__main__":
	main(argv)
