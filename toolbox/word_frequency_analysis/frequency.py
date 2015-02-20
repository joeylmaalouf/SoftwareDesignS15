""" Analyzes the word frequencies in a book downloaded from Project Gutenberg
	Joey L. Maalouf
"""
import operator
import string
import sys


def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	with open(file_name, "r") as readfile:
		#  read the file contents into a string
		text = readfile.read()
		#  strip everything before the start marker
		text = text[text.find("START OF THIS PROJECT GUTENBERG EBOOK"):]
		#  remove the start marker by trimming to the next newline
		text = text[text.find("\n"):]
		#  make case-insensitive by turning everything lowercase
		text = text.lower()
		#  remove all punctuation by "translating" it to empty strings
		text = text.translate(string.maketrans("", ""), string.punctuation)
		#  split, by default, splits on any whitespace character, leaving us with a list of just words
		return text.split()


def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequently occurring
	"""
	word_dict = {}
	for word in word_list:
		if word in word_dict:
			#  add to its existing count
			word_dict[word] += 1
		else:
			#  initialize its starting count
			word_dict[word] = 1
	#  return a list of tuples (to represent the dictionary) of length n, reversely sorted by value (occurence count)
	return sorted(word_dict.items(), key = operator.itemgetter(1), reverse = True)[:n]


def main(argv):
	top_words = get_top_n_words(get_word_list("./pg10148.txt"), 100)
	for pair in top_words:
		print(pair)


if __name__ == "__main__":
	main(sys.argv)
