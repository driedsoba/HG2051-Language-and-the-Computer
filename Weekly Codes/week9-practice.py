# # Week 09

# Overview
# * First-class-Functions
# * Higher-order-Functions
# * Recursive-Functions
# * Bigrams
# * N-grams
# * Collocations
# * Part-of-Speech-Tags

import nltk
# ## First-class Functions

# Functions in Python are just a special kind of object, and 
# you can use them in many ways that you can use other kinds of 
# objects, like integers, strings, etc.
def function(x):
    print(f'x={x}')

func = function   # reassignment
func('123')
func == function  # comparison

# This flexibility enables higher-order functions.

# ## Higher-order Functions
# Use `filter()` with `str.isdigit()` to filter out non-numbers 
# from a list of strings.
strings = 'one 2 three 4 five 6 seven 8'.split()
number_strings = list(filter(str.isdigit, strings))
print(number_strings)

# Now use `map()` with `int` to convert them all to integers.
numbers = list(map(int, number_strings))
print(numbers)

# Write a higher-order function that takes a text-normalization 
# function (such as `str.lower()`) and returns a new function that 
# takes a list of strings and applies the normalization function 
# to each one, returning a new list of strings.
def make_normalizer(func):
    def abc(strings):
        return [func(s) for s in strings]
    return abc

all_upper = make_normalizer(str.upper)
dont_panic = "don't panic".split()
print(dont_panic)
print(all_upper(dont_panic))
all_title = make_normalizer(str.title)
print(all_title(dont_panic))
print(make_normalizer(str.lower)(["DON'T", "Panic"]))

# ## Recursive Functions
# Write a recursive function to compute the fibonacci sequence, defined as:
# $$ fib(0) = 1 $$
# $$ fib(1) = 1 $$
# $$ fib(x) = fib(x-2) + fib(x-1) $$
def fib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)
print(fib(35))

# Try it out for a few values, like 3, 5, 10, 20, 40, ...

# Now try to write it iteratively.
def iterfib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        a = b = 1
        for _ in range(n - 1):
            a, b = b, a+b
    return b
iterfib(1000)

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
