""" Empirical testing of algorithm complexity """

import re
import time
import numpy as np
from matplotlib import pyplot
from bisect import bisect_left

def bisect_in(x, t):
    """ Uses bisect to check if x is in t.

        x: element to find
        t: sorted list

        Returns: boolean
    """
    i = bisect_left(t, x)
    return i != len(t) and t[i] == x

def load_words_as_list(skip_factor):
    """ Load a dictionary of words as a list.

        skip_factor: the step size to move through the textfile words.txt when
                     constructing the dictionary
        Returns: a list containing the words in the dictionary
    """
    f = open('words.txt','r')
    words = f.readlines()
    selected_words = []
    for i in range(0,len(words),skip_factor):
        selected_words.append(words[i].rstrip())
    f.close()
    return selected_words
    
def load_words_as_set(skip_factor):
    """ Load a dictionary of words as a set.

        skip_factor: the step size to move through the textfile words.txt when
                     constructing the dictionary
        Returns: a set containing the words in the dictionary
    """
    f = open('words.txt','r')
    words = f.readlines()
    selected_words = []
    for i in range(0,len(words),skip_factor):
        selected_words.append(words[i].rstrip())
    f.close()
    return set(selected_words)

def get_words(file_name):
    """ Grabs the words for spellchecking from the specified file.
    
        file_name: the file to spellcheck
        Returns: a list of all words in the input file
    """
    f = open(file_name,'r')
    s = f.read()
    f.close()
    return re.findall('\w+',s)

def spell_check_alg1(skip_factor, num_words_to_check):
    """ Algorithm 1 for spell checking
    
        skip_factor: the skip factor to use when constructing the dictionary
        Returns: the average time to spell check each word
    """
    all_words = load_words_as_list(skip_factor)
    words_to_spellcheck = get_words('const.txt')
    start_time = time.time()
    for i in range(len(words_to_spellcheck)):
        current_word = words_to_spellcheck[i].lower()
        spelled_correctly = False
        for w in all_words:
            if current_word == w:
                spelled_correctly = True
        if i + 1 == num_words_to_check:
            current_time = time.time()
            print "running time: %.10f" % (current_time - start_time)
            return current_time - start_time

def spell_check_alg2(skip_factor, num_words_to_check):
    """ Algorithm 2 for spell checking
    
        skip_factor: the skip factor to use when constructing the dictionary
        Returns: the average time to spell check each word
    """
    all_words = load_words_as_set(skip_factor)
    words_to_spellcheck = get_words('const.txt')
    start_time = time.time()
    for i in range(len(words_to_spellcheck)):
        current_word = words_to_spellcheck[i].lower()
        spelled_correctly = current_word in all_words
        if i + 1 == num_words_to_check:
            current_time = time.time()
            print "running time: %.10f" % (current_time - start_time)
            return current_time - start_time

def spell_check_alg3(skip_factor, num_words_to_check):
    """ Algorithm 3 for spell checking
    
        skip_factor: the skip factor to use when constructing the dictionary
        Returns: the average time to spell check each word
    """
    all_words = load_words_as_list(skip_factor)
    words_to_spellcheck = get_words('const.txt')
    start_time = time.time()
    for i in range(len(words_to_spellcheck)):
        current_word = words_to_spellcheck[i].lower()
        spelled_correctly = bisect_in(current_word,all_words)
        if i + 1 == num_words_to_check:
            current_time = time.time()
            print "running time: %.10f" % (current_time - start_time)
            return current_time - start_time

if __name__ == '__main__':
    """ select the algorithm to use for spell checking
        choices are:
            - spell_check_alg1
            - spell_check_alg2
            - spell_check_alg3
    """
    spell_check = spell_check_alg1
    n_trials = 1                   # the number of times to repeat a run
    """ Specifies the number of words of the constitution to spell check.  Note:
        we start from the beginning of the constitution and check until the
        word limit is reached
    """
    num_words_to_check = 2000
    make_plot = False               # Should we make a plot of running time versus input size?

    skip_factors = range(1,20)     # which skip factors to test 
    if not(make_plot):
        spell_check(1,num_words_to_check)
    else:
        total_words = len(load_words_as_list(1))
        trials = np.zeros((n_trials,len(skip_factors)))
        for n in range(n_trials):
            for i,skip in enumerate(skip_factors):
                trials[n,i] = spell_check(skip, num_words_to_check)
        pyplot.plot([float(total_words)/skip for skip in skip_factors],trials.mean(axis=0).T)
        ymin, ymax = pyplot.ylim()
        pyplot.ylim(0,ymax)
        pyplot.xlabel('Dictionary Size')
        pyplot.ylabel('Running Time (seconds)')
        pyplot.show()