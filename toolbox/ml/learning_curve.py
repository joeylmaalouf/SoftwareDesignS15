""" Exploring learning curves for classification of handwritten digits
	Joey L. Maalouf
"""


import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

num_trials = 50
train_percentages = range(5, 95, 5)
test_accuracies = numpy.zeros(len(train_percentages))

data = load_digits()
print(data.DESCR)

for i in range(len(train_percentages)):
	sum_score = 0.0
	for j in range(num_trials):
		X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size=train_percentages[i]/100.0)
		model = LogisticRegression(C = 1.0)
		model.fit(X_train, y_train)
		sum_score += model.score(X_test, y_test)
	test_accuracies[i] = sum_score/num_trials

fig = plt.figure()
plt.plot(train_percentages, test_accuracies)
plt.xlabel("Percentage of Data Used for Training")
plt.ylabel("Accuracy on Test Set")
plt.show()
