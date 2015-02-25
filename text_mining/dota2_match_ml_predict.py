""" Defense of the Ancients 2 Match Machine Learning Prediction
	This program reads in the data file created by the match analysis and
	uses the hero matchup information to train a neural network. Hopefully,
	given any 5v5 set of hero ids, the network will be able to predict which
	team will win based on the hero matchups.

	Joey L. Maalouf
"""


#  module imports
from cPickle     import load
from numpy       import array
from os.path     import exists
from pprint      import pprint
from sklearn.svm import SVC
from sys         import argv


def parse(data, x, y):
	for game in data:
		x.append([float(player["hero_id"]) for player in game["players"]])
		y.append(game["radiant_win"])
	data = zip(x, y)
	try:
		for i in range(len(x)):
			if len(x[i]) < 10:
				del x[i]
				del y[i]
	except IndexError:
		pass


def main(argv):
	data_file = "dota2_match_data_list.txt"
	game_details = {}
	if exists(data_file):
		file_object = open(data_file, "rb")
		game_details = load(file_object)
		file_object.close()

	size = len(game_details)
	print(str(size)+" samples")
	train_xy = game_details.values()[:-size/4]
	train_x, train_y = [], []
	test_xy = game_details.values()[-size/4:]
	test_x, test_y = [], []

	parse(train_xy, train_x, train_y)
	parse(test_xy, test_x, test_y)

	train_x = array(train_x)
	train_y = array(train_y)
	test_x = array(test_x)
	test_y = array(test_y)

	svc = SVC(kernel = "linear")
	svc.fit(train_x, train_y)
	prediction = svc.predict(test_x)
	results = [int(prediction[i] == test_y[i]) for i in range(len(prediction))]
	accuracy = float(sum(results))/len(results)
	print("{:0.2f}".format(accuracy*100)+"% accuracy")


if __name__ == "__main__":
	main(argv)
