# # Week 11

# This week covers supervised classification.

# Overview:

# * Supervised Classification
# * Evaluation
# * Decision Trees


# ## Machine Learning
# You can get a program to make decisions and act intelligently based on 
# its inputs using programming constructs like conditional expressions, 
# loops, etc., but it is often infeasible to construct programs for large, 
# complicated, or ambiguous tasks. Machine Learning (ML) is how you can get 
# computers to respond to inputs without hard-coded rules by learning from 
# examples. The programmer's job is thus to teach the program how to learn 
# from examples it is given.

# ## Supervised Classification
# Supervised classification is a kind of machine learning where examples 
# contain the correct labels that you want the system to predict. The system 
# then extracts features from the examples and builds a model that helps it 
# infer the correct label given the features. Then, when encountering a new, 
# unlabeled instance, it guesses the likely label based on the instance's 
# feature similarity to other examples.

# ### Feature Extraction

# Given an instance, you need to produce features that the system can learn 
# from. Good features are highly predictive of certain labels while excluding 
# the other labels. Sometimes simple features work well, such as "word ends in 
# `ed`", and other times complex features are more distinguishing, such as
# "word ends in `ed` and previous word is tagged `MD`".

# Write a feature extraction function for classifying names as male or female:
def gender_features(name):
    feats = {
        f'last_letter={name[-1]}': True,
        f'first_letter={name[0]}': True,
        f'last_two_letters={name[-2:]}': True
        }
    return feats

print(gender_features('Michael'))
print(gender_features('Michelle'))
print(gender_features('Francis'))
print(gender_features('Frances'))

# Now try it out with a Naive Bayes classifier. First load some data:
import random
from nltk.corpus import names

labeled_names = (
    [(name, 'male') for name in names.words('male.txt')]
    + [(name, 'female') for name in names.words('female.txt')]
)
random.shuffle(labeled_names)  # why do this? (hint: take a look at the next step)
labeled_names[0]

# Now create training and test splits (set aside 10% of the data for testing data)
index = int(1/10 * len(labeled_names))  # TODO: find the index that splits 1/10 of the data
test_set = labeled_names[:index]  # TODO: use index and labeled_names to get 1/10 of the data
train_set = labeled_names[index:]  # TODO: use index and labeled_names to get 9/10 of the data
print('test', len(test_set),
      'male:', sum(1 for _, label in test_set if label == 'male'),
      'female:', sum(1 for _, label in test_set if label == 'female'))
print('train', len(train_set),
      'male:', sum(1 for pair in train_set if pair[1] == 'male'),
      'female:', sum(1 for _, label in train_set if label == 'female'))
# TODO: inspect the train set, try out gender_features() on an instance, etc.
print(train_set[0])

gender_features(train_set[0][0])
train = [(gender_features(name), label) for name, label in train_set]  # TODO: compute gender_features for each (name, label) in train_set, pair result with label
test = [(gender_features(name), label) for name, label in test_set]  # TODO: do the same for the test set
import nltk
classifier = nltk.NaiveBayesClassifier.train(train)  # Train a NB classifier with the training data
print(classifier.classify(gender_features('Michael')))
print(classifier.classify(gender_features('Michelle')))
print(classifier.classify(gender_features('Francis')))
print(classifier.classify(gender_features('Frances')))
print()
print(nltk.classify.accuracy(classifier, test))

# #### Gender identification for Japanese
# Now do the same for Japanese names. The ENAMDICT file contains over 
# 100,000 Japanese names, annotated as (m) for male and (f) for female 
# (and some others for unspecied, family names, etc., which we will ignore). 
# First download the file from here: https://hg2051-ntu.github.io/static/code/enamdict
from urllib import request
raw_data = request.urlopen('https://hg2051-ntu.github.io/static/code/enamdict').read()
# And decode from UTF-8. We will need to parse this file (probably with regular 
# expressions) in order to generate (name, label) pairs. So after decoding, inspect 
# the data to get an idea of how to parse it:
data = raw_data.decode('utf-8')
print(data[:1000])
# The name in kanji is the first letter(s) of each line followed by the transliteration 
# in hiragana inside `[` and `]` characters, then the transliteration in romaji 
# inside `/` and `/`. Inside `/` and `/` is also the gender label inside of 
# parentheses. Assuming we want to model our features on the kanji name, we 
# can ignore all the transliteration data. So we need to first capture the 
# name (`r'^(\w+) \['`), followed by anything (`.*`) until we see the label 
# (`\(([mf])\)`). Since we only match on `m` and `f`, we ignore any names with 
# other labels.
import re
jpn_data = []
for line in data.splitlines():
    m = re.match(r'^(\w+) \[.*\(([fgm])\)', line)  # TODO: write a regular expression to capture the name and gender
    if m:
        jpn_data.append(m.groups())
print(jpn_data[-1])

# As before, we need to process the data for training and testing the model.
random.shuffle(jpn_data)
# the japanese data is too big! just use a tenth for now
jpn_data = jpn_data[:int(len(jpn_data)/10)]

index = int(len(jpn_data) / 10)
j_train_set = jpn_data[index:]
j_test_set = jpn_data[:index]
print('train', len(j_train_set),
      'm:', sum(1 for pair in j_train_set if pair[1] == 'm'),
      'f:', sum(1 for _, label in j_train_set if label == 'f'))
print('test', len(j_test_set),
      'm:', sum(1 for _, label in j_test_set if label == 'm'),
      'f:', sum(1 for _, label in j_test_set if label == 'f'))
gender_features(j_train_set[0][0])
# The `gender_features()` may be relevant for Japanese data as well, as 
# long as it doesn't have any English-specific features.
j_train = [(gender_features(name), label) 
        for name, label in j_train_set]  # TODO: compute gender_features() for j_train_set, pair each with label

j_test = [(gender_features(name), label) 
        for name, label in j_test_set]  # TODO: do the same for j_test_set
print(gender_features('太郎'))
j_classifier = nltk.NaiveBayesClassifier.train(j_train)
print('太郎', j_classifier.classify(gender_features('太郎')))
print('文美', j_classifier.classify(gender_features('文美')))
print('香月', j_classifier.classify(gender_features('香月')))
print('良男', j_classifier.classify(gender_features('良男')))
print('恵里香', j_classifier.classify(gender_features('恵里香')))
print(nltk.classify.accuracy(j_classifier, j_test))

# ### Feature Selection
# Not all features are useful, so the task of feature selection tries 
# to choose the best ones. There are many methods for selecting relevant 
# features, but for now let's just see what the model thinks are the most 
# informative ones:
classifier.show_most_informative_features(15)
j_classifier.show_most_informative_features(15)
exit()
# ## Evaluation
# In order to evaluate supervised ML systems, we need gold test data. It 
# is imperative that you do not evaluate your system on the data that you 
# trained it on, as the evaluation will be meaningless at best and often 
# deceptive. The first task is to split your data into separate sets for 
# training and evaluation.

# ### Data splits
# A normal proportion of test data to the rest is 10:90, and the remainder 
# often sets another 10% aside as development data, with the final remainder 
# as training data:

# |Training-(80%)-------------------|Dev--(10%)|Test-(10%)|

# Note that the terminology for these splits is sometimes inconsistent.

# * training : used for model learning; standard
# * development : used to evaluate a model for refinement or tuning
#   * sometimes called `validation` or `tuning` data
#   * sometimes refers to `training` + `validation`
# * test : used for final evaluation of a model; standard
#   * sometimes called `evaluation` or `holdout` or `unseen` data

# See [this Wikipedia article](https://en.wikipedia.org/wiki/Training,_validation,_and_test_sets) 
# or [this Google ML course](https://developers.google.com/machine-learning/crash-course/training-and-test-sets/splitting-data) 
# for more info.

# How you split the data is important. Simply taking contiguous blocks 
# or shuffling the data can lead to unrepresentative samples. Often you 
# need to look at the data first in order to decide how to split.

# ### Accuracy, Precision, Recall, and F-score

#                           Gold Values:
#                   True Positive   |   False Positive
# System Output:    ----------------------------------
#                   False Negative  |   True Negative

# Define the following terms:
# * Accuracy: `acc = (TP + TN) / (TP + FP + FN + TN)`
# * Precision: `P = TP / (TP + FP)`
# * Recall: `R = TP / (TP + FN)`
# * F-score: `F = (2 * P * R) / (P + R)`

# ## Decision Trees
# Decision trees are a machine learning model that learns individual 
# decisions that best split the data into separate categories. Entropy 
# and Information-gain are metrics used to determine how well a feature 
# splits the data.

# ### Entropy
# Entropy is defined as

# $ - \sum_x{p(x) * log_2{p(x)}} $

# For $p(x)$ we can use the `freq()` method of `nltk.FreqDist` 
# which returns the frequency of some item as the proportion of 
# the total:
fd = nltk.FreqDist('mmfff')
fd.freq('m')

# Now given some list of labels (extracted from the gold instances), 
# we can calculate the entropy of that list as follows:
import math
def entropy(labels):
    fd = nltk.FreqDist(labels)
    return -sum(fd.freq(x) * math.log2(fd.freq(x)) for x in labels)
    # TODO: calculate and return entropy
entropy(['m', 'm', 'f', 'f', 'f'])
entropy('mmmmmm')
entropy('fffff')

# ### Information Gain
# Information gain is defined for this task as the difference in 
# the entropy of a current sent of data and the set resulting by 
# splitting it on some feature.

# #### Train a DecisionTreeClassifier
# Now try to train a `nltk.DecisionTreeClassifier`. You can use 
# the same data as before with the feature dictionaries.
dt_classifier = nltk.DecisionTreeClassifier.train(train)
print(nltk.classify.accuracy(dt_classifier, test))
j_dt_classifier = nltk.DecisionTreeClassifier.train(j_train)  # may take a long time!
print(nltk.classify.accuracy(j_dt_classifier, j_test))

# The accuracy did not change for the English data but it went up a bit 
# for the Japanese data. Different models (Naive Bayes, Decision Tree, 
# etc.) have different characteristics and may do better on certain kinds 
# of data than others. Sometimes you can just try out a few to find one 
# that works well, but sometimes the cost (time, money) of training a 
# new model prevents you from exploring all options, so it is good to 
# develop some intuition about the kinds of data that each does well on.
