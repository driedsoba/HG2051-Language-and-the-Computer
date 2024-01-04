# # Week 09

# Overview

# * Review
#   * Assignment
#   * Equality
#   * Conditionals
#   * Sequences
#   * Loops and Comprehensions
# * Style
# * Advanced Functions
# * Testing
# 
# * [**Bigrams**](#Bigrams)
# * [**N-grams**](#N-grams)
# * [**Collocations**](#Collocations)
# * [**Part-of-Speech Tags**](#Part-of-Speech-Tags)

# # Review
# Here we dig a little deeper into some familiar concepts.
#
# ## Assignment
#
# In Python, assignment associates a variable name to some data.
x = 3
y = [x]
print(y)

# More than one variable can be assigned to the same data.
z = x
z == x

# Variables can be reassigned to other data (it doesn't change other 
# variables that pointed to the original data).
x = 7
z == x

# Modifying mutable data does not change the assignment.
y = [x]
y == [7]
x = 5
y == [5]
q = y
q == y
y[0] = 5
q == y

# ## Equality
# `==` tests if things are "equal". `is` tests if things are the same object.

# "Identical twins are equal in many ways, but they are not the same entities."
x = ['a']
y = x
y == x and y is x
y = ['a']
y == x
print(y is x)

# ## Conditionals
# `if` statements check the "boolean context" of an expression (whether 
# an expression is considered `True` or `False`). You can use the `bool()` 
# function to test the boolean value of an expression. Python types have 
# some (perhaps arbitrary, but useful) boolean values:

# * Empty strings, lists, tuples, dicts, sets, etc. are `False`, non-empty 
# ones are `True`
# * `0` values for floats and ints are `False`, all others are `True`
x = {}
if x:
    print('x is True in a boolean context')

# Be careful when to use `if`, `elif`, and `else` for successive tests.
z = 23
if z > 0:
    print('z is greater than 0')
elif z > 10:
    print('z is greater than 10')

# `any()` and `all()` return `True` if any/all of a sequence of 
# expressions are `True`
print(any([True, False, False]))
print(all([True, False, False]))

# ## Sequences
# Tuples are defined using commas, but parentheses are used for 
# grouping to avoid ambiguity. As a special case, empty parentheses 
# indicate an empty tuple.
x = 1,
y = 1, 2
z = ()
print('{} {}'.format((1, 2), 3))

# ## Loops and Comprehensions
# `for` loops go over each item in some iterable:
for i in range(1,10,2):
    print("i =", i)

# `while` loops loop until some condition is met. Transform the 
# `for`-loop above into a `while`-loop.
i = 1
while i < 10:
    print(i)
    i = i+2

# Now transform the following `while`-loop into the equivalent `for`-loop.
i = 20
while (i > 0):
    print("i =", i)
    i -= 1

for i in range(20,0,-1):
    print ("i = ",i)

# List comprehensions can put multiple `for`-loops in one line and 
# generate a list, but they can be hard to read. Transform the following 
# list comprehension into `for`-loops.
print([i + j for i in 'abc' for j in 'xyz'])

for i in 'abc':
    for j in 'xyz':
        print (i+j)

# Without the square brackets `[]`, the same construct becomes a 
# "generator expression", which can be used in iterable contexts.
print(' '.join([i + j for i in 'abc' for j in 'xyz']))
print(' '.join(i + j for i in 'abc' for j in 'xyz'))

# Generator expressions, when appropriate, can be more efficient 
# than list comprehensions as they do not need to create the entire 
# list, which can save memory:
print(sum([i for i in range(50000000)]))  # this uses ~2GB of memory to compute the sum
print(sum(i for i in range(50000000)))  # this uses almost nothing

# # Style
# Coding style conventions are used to keep code looking consistent 
# and predictable. It does not change the correctness or efficiency 
# of the code, but it helps to avoid bugs and to improve the readability 
# of the code.

# The Python style conventions are given by [PEP-8](https://www.python.org/dev/peps/pep-0008/). 
# General things to note are when to use whitespace and how to 
# name variables, functions, classes, etc. Sometimes people disagree 
# with the conventions, and this is ok if there's a good reason. 
# Consistency within your own code is important.

# For example, sometimes I will align the operator when I have multiple 
# variables being assigned. I find it more legible, but the guidelines 
# say it is difficult to maintain.
# noun        = 'dog'
# verb        = 'sat'
# preposition = 'in'

# # Advanced Functions
# We have used functions that do take parameters and return values. 
# But there are other kinds of functions.
# Functions that operate on some input should return a new value 
# without changing the input or change the input and return nothing, 
# but not both.
def double(x):
    return x * 2

# Accumulators build up something (e.g., a list or dict) and return it. 
# We have used these.
def word_lengths(words):
    lens = []
    for word in words:
        lens.append(len(word))
    return lens

print(word_lengths(['What', 'is', 'the', 'length', 'of', 'each', 'word', '?']))

# The `yield` statement is like `return` but it doesn't exit the function:

def word_lengths(words):
    for word in words:
        yield len(word)

print(word_lengths(['What', 'is', 'the', 'length', 'of', 'each', 'word', '?']))

# It doesn't return a list but a "generator". You can iterate over 
# generators (e.g., in a `for`-loop), get successive items with 
# [next()](https://docs.python.org/3/library/functions.html#next), 
# cast to a list, etc.
print(list(word_lengths(['What', 'is', 'the', 'length', 'of', 'each', 'word', '?'])))

# Recursive functions call themselves (but be careful they don't 
# get stuck!). The `fib()` function below computes the 
# [Fibonacci number](https://en.wikipedia.org/wiki/Fibonacci_number) of `x`.
def fib(x):
    if x <= 2:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)
    
# Recursive functions look very elegant and closely resemble their 
# mathematical definitions, but they sometimes have bad performance. 
# You can create iterative versions of recursive functions that 
# perform much better, but they are harder to read (and often harder 
# to write).

# Transform the recursive function `fib()` to an iterative function:
def fib2(x):
    if x <= 2:
        return 1
    a, b = 1, 1
    for i in range(3, x):
        tmp = b
        b += a
        a = tmp
    return a + b
print(fib(40))
print(fib2(40))

# Function names are variables like anything else in Python. You 
# can reassign them and pass them as variables:
fib3 = fib2

# The following function gets the last letter of a string:
def lastletter(s):
    return s[-1]

print(lastletter('dog'))

# Some functions take other functions as arguments. For example, 
# `sorted()` takes a `key` parameter which is a function used 
# to determine how to sort. Using `lastletter()` above, we can 
# sort a list of words by the last letter of each word:
print(sorted('The dog chased the cat'.split(), key=lastletter))

# Or we could use `len()` to sort by the length of each word:
print(sorted('What does this sentence look like sorted by length ?'.split(), key=len))

# `map()` is a function that takes another function and applies 
# it to everything in an iterable:
word_lengths = list(map(len, ['What', 'is', 'the', 'length', 'of', 'each', 'word', '?']))
print(word_lengths)

# # Testing

# * unit tests
# assert my_function(some_value) == expected_value

# * regression tests
# * performance tests
# * stress tests
import timeit
timeit.timeit('fib2(30)', setup='from __main__ import fib2', number=10)

import nltk

# ## Bigrams

# Bigrams are sequential pairs of items in a list. With language data, 
# these items are generally words or characters. The bigrams (and 
# n-grams in general) are like a sliding window of a small sequence 
# of the data, and capture partial order information (e.g., "the" 
# precedes "dog" in *the dog barked*). The bigrams for the sentence 
# *Bigrams and n-grams are useful tools for computational linguists.* 
# are as follows (with list indices indicated):

#       Bigrams and n-grams are useful tools for computational linguists .
#       0       1   2       3   4      5     6   7             8         9 10
# 0:2   Bigrams and
# 1:3           and n-grams
# 2:4               n-grams are
# 3:5                       are useful
# 4:6                           useful tools
# 5:7                                  tools for
# 6:8                                        for computational
# 7:9                                            computational linguists
# 8:10                                                         linguists .

# **Task:** write a function to take an sequence and return a list 
# of its bigrams. Compare your results with `nltk.bigrams()`
def bigrams(seq):
    """
    Return the list of bigrams for *seq*.
    Each bigram on the list should be a tuple.
    """
    return [tuple(seq[i:i+2]) for i in range(len(seq) - 1)]

words = 'Bigrams and n-grams are useful tools for computational linguists .'.split()
print('Test:', list(bigrams(words)))
print()
print('NLTK:', list(nltk.bigrams(words)))
print()
print('Equal?', list(bigrams(words)) == list(nltk.bigrams(words)))

# ## N-grams
# Sometimes bigrams do not give enough context (they are not a 
# big enough window into the sequence). N-grams are the general 
# form of bigrams, where N=2. Write a function that takes a sequence 
# and a number `n` and returns the list of n-grams for the sequence. 
# Note that if `n` is greater than the length of the list, an empty 
# list is returned.
def ngrams(seq, n):
    """
    Return the list of n-grams for *seq* of length *n*.
    
    Each n-gram should be a tuple. If *n* is greater than the length
    of *seq*, an empty list is returned. *n* must be greater than 0.
    """
    return []
words = 'Bigrams and n-grams are useful tools for computational linguists .'.split()
print('1-grams:', list(ngrams(words, 1)))
print()
print('2-grams:', list(ngrams(words, 2)))
print()
print('3-grams:', list(ngrams(words, 3)))
print()
print('20-grams:', list(ngrams(words, 20)))
print()
print('Equal?', list(ngrams(words, 3)) == list(nltk.ngrams(words, 3)))

# ## Collocations
# Note that some n-grams, such as `('are', 'useful')` are probably 
# more frequent than others, such as `('Bigrams', 'and')`. N-grams 
# whose components co-occur frequently are called "collocations". 
# With an appropriate metric you can compute a collocation score 
# for these, which could also be used as a threshold. Mutual 
# information (MI) is a measure using the *observed frequencies* 
# (O) and *expected frequencies* (E):

# $$ MI = log \frac{O}{E} $$

# The observed frequency is how often we see the n-gram in the 
# data. The expected frequency is how often we expect to see it 
# given the frequencies of its components. Here is one way to 
# define collocations (adapted from the reading):
from operator import itemgetter

# # itemgetter() is a function that takes a number n and returns a
# # function which takes a sequence and returns the item at index n
first = itemgetter(1)

def collocations(words):
    # Count the words and bigrams
    wfd = nltk.FreqDist(words)
    pfd = nltk.FreqDist(bigrams(words))

    scored = [((w1,w2), score(w1, w2, wfd, pfd)) for w1, w2 in pfd]
    ## sort according to the score
    scored.sort(key=first, reverse=True)
    return [p for (p,s) in scored]


def score(word1, word2, wfd, pfd, power=3):
    '''return the collocation score f(w1,w2)^power/(f(w1)*f(w2))'''
    freq1 = wfd[word1]
    freq2 = wfd[word2]
    freq12 = pfd[(word1, word2)]
    return freq12 ** power / float(freq1 * freq2)

# Now we can test it:
from nltk.corpus import webtext

for file in webtext.fileids():
    words = [word.lower() for word in webtext.words(file) if len(word) > 2]
    print (file, [w1+' '+w2 for w1, w2 in collocations(words)[:15]])

# **Task:** Rewrite `collocations()` that takes a `threshold` 
# parameter to filter out collocations whose score doesn't 
# meet the threshold.



# ## Part-of-Speech Tags
# Part-of-speech tags, also called "word categories", are a 
# shallow annotation on top of words that give a hint as to 
# their syntactic function. It is not the case that all languages 
# have the same parts of speech, and some linguists even reject 
# the notion altogether, but for computational linguists they 
# are often useful for modeling language.

# When serialized, POS tags are conventionally written following 
# the word they annotate, separated with a slash:

# The/DT artist/NN will/RB record/VBZ a/DT new/JJ record/NN ./.

# In Python, these may be loaded as a list of pairs:

postags =  [('The', 'DT'), ('artist', 'NN'), ('will', 'RB'), ('record', 'VBZ'),
   ('a', 'DT'), ('new', 'JJ'), ('record', 'NN'), ('.', '.')]

# The NLTK has several functions defined for tagging text and 
# working with POS-tagged data. If you have a list of words, you 
# can use a basic tagger with `nltk.pos_tag()`. You might also 
# want to use `nltk.word_tokenize()` to break a sentence into a 
# list of words as NLTK expects. Try them out:
import nltk
import nltk.tag
words = "This is a sentence." # first tokenize this sentence

# # then pos-tag the words

# If you have tagged text (in the `word/NN` serialization), you 
# can use `nltk.tag.str2tuple()`. Try it out (you can use the 
# example above):

# # convert a word/TAG pair to a tuple

# When working with multilingual data, it would probably help 
# to ensure the data from different languages uses the same set 
# of tags. The `nltk.map_tag()` function can map from a known 
# tag set to another, and the 'universal' tags are generalized 
# to be relevant for many languages.

print(nltk.map_tag('en-ptb', 'universal', 'NN'))

# **Task:** Try to convert the tags for the sentence above into universal tags.
