from pattern.web import Google, plaintext
from sys import argv


def main(argv):
	for result in Google().search(argv[1]):
		print(result.url)
		print(plaintext(result.text))
		print("")


if __name__ == "__main__":
	main(argv)
