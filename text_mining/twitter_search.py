from pattern.en import sentiment
from pattern.web import Twitter
from sys import argv


def main(argv):
	if len(argv) < 3:
		argv.append(10)
	search_term = argv[1]
	search_count = int(argv[2])
	sent_polr = []
	sent_subj = []
	t = Twitter()
	i = None
	print("")
	for tweet in t.search(argv[1], start = i, count = search_count):
		print(tweet.text)
		print("")
		i = tweet.id
		sent = sentiment(tweet.text)
		sent_polr.append(sent[0])  #  between -1.0 and 1.0
		sent_subj.append(sent[1])  #  between  0.0 and 1.0
	polr = sum(sent_polr)/len(sent_polr)
	subj = sum(sent_subj)/len(sent_subj)
	feeling = "negative" if polr < 0.0 else "positive" if polr > 0.0 else "neutral"
	objsubj = "objective" if subj < 0.5 else "subjective" if subj > 0.5 else "neutral"
	print("Mean sentiment polarity: "+str(polr)+".")
	print("The overall feeling about "+search_term+" is "+feeling+"!")
	print("Mean sentiment subjectivity: "+str(subj)+".")
	print("The subjectivity about "+search_term+" is "+objsubj+"!")
	print("")


if __name__ == "__main__":
	main(argv)
