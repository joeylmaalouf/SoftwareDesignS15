from pattern.web import Twitter
from sys import argv


def main(argv):
	t = Twitter()
	i = None
	for tweet in t.search(argv[1], start=i, count=10):
		print(tweet.text)
		print("")
		i = tweet.id


if __name__ == "__main__":
	main(argv)
