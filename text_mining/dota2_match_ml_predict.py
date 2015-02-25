""" Defense of the Ancients 2 Match Machine Learning Prediction
	This program reads in the data file created by the match analysis and
	uses the hero matchup information to train a neural network. Hopefully,
	given any 5v5 set of hero ids, the network will be able to predict which
	team will win based on the hero matchups.

	Joey L. Maalouf
"""


#  module imports
from cPickle import load
from os.path import exists
from pprint  import pprint
from sys     import argv


def main(argv):
	data_file = "dota2_match_data_list.txt"
	game_details = {}
	if exists(data_file):
		file_object = open(data_file, "rb")
		game_details = load(file_object)
		file_object.close()
	train_x = []
	train_y = []
	for game in game_details.values():
		train_x.append([player["hero_id"] for player in game["players"]])
		train_y.append(game["radiant_win"])
	#  pprint(zip(train_x, train_y))
	#  use thenao? train neural net here


if __name__ == "__main__":
	main(argv)
