from pattern.web import Twitter
from sys import argv


def main(argv):
	if len(argv) < 3:
		argv.append(10)
	t = Twitter()
	i = None
	print("")
	for tweet in t.search(argv[1], start = i, count = int(argv[2])):
		print(tweet.text)
		print("")
		i = tweet.id


if __name__ == "__main__":
	main(argv)
