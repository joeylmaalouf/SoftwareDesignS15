""" Defense of the Ancients 2 Match Machine Learning Prediction
	This program reads in the data file created by the match analysis and
	uses the hero matchup information to train some machine learning model.
	Hopefully, given any 5v5 set of hero ids, the model will be able to
	predict which team will win based on the hero matchups.

	Joey L. Maalouf
"""


#  module imports
from cPickle     import load
from numpy       import array
from os.path     import exists
from pprint      import pprint
from random      import sample
from sklearn.svm import SVC
from sys         import argv


def split_data(data):
	""" Given a list of data, randomly select 3/4 of it
		as training data and the rest as testing data.
	"""
	num_train = 3*len(data)/4
	shuffled = sample(data, len(data))
	return (shuffled[num_train:], shuffled[:num_train])


def process(data):
	""" Given a list of data, return two lists of
		input features (x) and corresponding output (y).
	"""
	x, y = [], []
	for game in data:
		x.append([float(player["hero_id"]) for player in game["players"]])
		y.append(game["radiant_win"])
	try:
		for i in range(len(x)):
			if len(x[i]) < 10:
				del x[i]
				del y[i]
	except IndexError:
		pass
	return (x, y)


def main(argv):
	#  ----  LOAD DATA  --------------------------------------------------------
	data_file = "dota2_match_data_list.txt"
	game_details = {}
	if exists(data_file):
		file_object = open(data_file, "rb")
		game_details = load(file_object)
		file_object.close()
	print(str(len(game_details))+" samples")

	#  ----  PROCESS DATA  -----------------------------------------------------
	(train_xy, test_xy) = split_data(game_details.values())
	(train_x, train_y) = process(train_xy)
	(test_x, test_y) = process(test_xy)


	#  ----  CREATE MODEL  -----------------------------------------------------
	svc = SVC(kernel = "linear")
	svc.fit(train_x, train_y)
	prediction = svc.predict(test_x)
	
	#  ----  GET OUTPUT  -------------------------------------------------------
	results = [int(prediction[i] == test_y[i]) for i in range(len(prediction))]
	accuracy = float(sum(results))/len(results)
	print("{:0.2f}".format(accuracy*100)+"% accuracy")


if __name__ == "__main__":
	main(argv)
