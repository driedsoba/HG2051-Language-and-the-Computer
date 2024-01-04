# # Week 04

# Overview:

# Python Topics:
#   Dictionaries
#     
#   {}                        # an empty dictionary
#     {'a': 1, 'b': 2, 'c': 3}  # a dictionary mapping 'a' to 1, 'b' to 2, and 'c' to 3
#   
#   Functions
    
#     def add(x, y):
#         """Add *x* and *y* and return the result."""
#         return x + y
    
#   Modules
#     Make a Python module (file):
    
#     # my_module.py
#     def greet(name):
#         print('Hi,' name)
#     
#     Then later you can import and use it:
#     
#     >>> import my_module
#     >>> my_module.greet('everyone')
#     Hi, everyone
#     
# NLTK Topics:
#   Conditional Frequency Distributions
#     
#     import nltk
#     # make a conditional frequency distribution of bigrams
#     nltk.ConditionalFreqDist([('the', 'dog'), ('dog', 'barked'), ('barked', '.')])
   
# Dictionaries
# Python dictionaries (abbreviated "dict", after the type dict (https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)) 
# are mappings between keys and values. For instance:
# 
points = {
    'Ashley': 9,  # Ashley has 9 points
    'Blake': 6,   # Blake has 6 points
    'Charlie': 7  # Charlie has 7 points
}
# 
# Keys must be hashable (https://docs.python.org/3/glossary.html#term-hashable), 
# which often means immutable (cannot change). For example, strings and integers 
# are good keys, but a list cannot be a key because you can append items to or 
# remove items from it. Values, however, can be any Python type and do not need 
# to be unique.
# Like sets (https://docs.python.org/3/library/stdtypes.html#set), dictionaries 
# must have unique keys, and they allow for fast lookup of keys and values.

# Dictionaries are generally created using braces (`{}`) with keys and values 
# delimited by a colon (`:`) and key:value pairs delimited by commas (`,`):
# 
{}                # an empty dict
{'a': 1, 'b': 2}  # a dict mapping strings to integers
{1: 'a', 2: 'b'}  # a dict mapping integers to strings
{'a': 1, 1: 'a'}  # a heterogeneous dict (in this case it's a bidirectional mapping)

# The braces are short-hand for the `dict()` function, which creates mappings 
# based on lists of pairs. The `dict()` function is especially useful when paired 
# with the `zip()` function.
# 
>>> dict()                      # an empty dict
{}
>>> dict([('a', 1), ('b', 2)])  # a dict mapping strings to integers
{'a': 1, 'b': 2}
>>> dict(zip('abc', [1,2,3]))
{'a': 1, 'b': 2, 'c': 3}
# 
# Until very recently (Python 3.6 or 3.7), there was no ensured order to the keys 
# in a dictionary (and the same for sets), unlike with [lists](https://docs.python.org/3/library/stdtypes.html#list). 
# It is still good practice to avoid relying on the order of items in a dictionary 
# or set, as your code may be run on older versions of Python at some point.

# ### Dictionary Methods
my_dict = {}                          # create empty dict
print(my_dict)                        # inspect
my_dict.update([('a', 1), ('b', 2)])  # update with list of pairs
print(my_dict)                        # inspect
my_dict.update({'c': 3, 'd': 4})      # update with another dict
print(my_dict)                        # inspect
my_dict.update({'d': -4, 'e': 5})     # reused keys get overwritten, new keys inserted
print(my_dict)                        # inspect
print(my_dict.keys())                 # get a 'view' of the keys
print(my_dict.values())               # get a 'view' of the values
print(my_dict.items())                # get a 'view' of the (key, value) pairs
print(my_dict.get('a'))               # get the value of key 'a'
print(my_dict.get('z', 26))           # if the key doesn't exist, a default value is returned
print(my_dict.pop('b'))               # pop() requires a key, returns the value
print(my_dict)                        # ensure the popped item is gone
print(my_dict.popitem())              # popitem() pops some (key,  value) pair

# ### Dictionary Operations
my_dict = dict(zip('abcde', range(1,6)))  # create a new dict
print(my_dict)                            # inspect
print('e' in my_dict)                     # test if 'e' is a key
print(5 in my_dict)                       # doesn't work for values
print(my_dict['c'])                       # get the value of 'c'
print(my_dict['z'])                       # but if the key doesn't exist it's an error
print(my_dict['f'] = 6)                   # set new key 'f' to 6
print(my_dict['a'] = -1)                  # give 'a' a new value
print(my_dict)                            # inspect
for key in my_dict:                       # iteration is over the keys
    print(key)
print(list(my_dict))                      # list() (and sorted(), reversed(), etc.) is also iteration
print(len(my_dict))                       # return the number of key:value pairs
del my_dict['a']                          # remove a single key:value pair
print(my_dict)                            # inspect

# ## Functions
# Sometimes you need to do the same thing in multiple places in your code. 
# For instance, you may want to compute the average length of sentences for 
# one corpus and then again later for another corpus. Rather than copying 
# the code to compute the average (or whatever it is you want to do), you 
# can put the relevant code in a function and call the function multiple 
# times instead. This method has several advantages:
#   * You don't have to write as much code. `average(lengths)` is easier than 
#     `sum(lengths) / len(lengths)` (and moreso with more complicated functions!).
#   * If you have a bug in your reused code, or if you want to change how it 
#     works, you only need to change it in one place and it will be fixed for 
#     all places that call the function.
#   * Related to the above, if you don't use functions and you fix a bug in, 
#     or change, the relevant code, you may introduce other, hard-to-detect 
#     bugs by forgetting to change the code equivalently in all locations.
#   * Function names can be descriptive and make the code easier to read. When 
#     you see `average(lengths)`, it is clear that it returns the average length, 
#     and this is less clear with `sum(lengths) / len(lengths)`.

# ### The Anatomy of a Function
# Functions are defined using the reserved keyword `def`, followed by the function 
# name and any parameters in parentheses, followed by a colon. All code related to 
# the function then follows, indented deeper than the level `def` was on. The following 
# diagrams the anatomy of a function:
# 
# #    ,-----function name
# #    |
# #    |  ,--,--parameters
# #    |  |  |            ,--- docstring (optional) is defined between
# #    V  V  V            |    the colon and the function's code
# def add(x, y):  #       V
#     """Add *x* and *y* and return the result."""
#     total = x + y
#     return total
# #### <-- function body is indented (conventionally 4 spaces)
# 
# Execute the following cell so the `add()` function is available:
# def add(x, y):
#     """Add *x* and *y* and return the result."""
#     total = x + y
#     return total
# ### Calling Functions

# In order to call a function, type the function name and its arguments. 
# The arguments (`1` and `2`, below) are assigned to the parameters `x` 
# and `y` for the function body of `add()`.

# print(add(1, 2))

# Note that the variables `x`, `y`, and `total` are no longer available 
# when the function returns, or if they were defined before the function 
# was called, their values outside of the function did not change:

# total = 0
# add(1, 2)
# print(total)

# The return value can be assigned to a variable or used in another expression:

# x = add(1, 2)
# print('1 + 2 =', add(1, 2))

# ### Return Values
# The expression after `return` in a function is what is returned by the function 
# (as `add(1, 2)` returned `3` above). If the function did not have a `return` 
# statement, the special value of `None` is returned. Try out `add2()` and see 
# the difference:

# def add2(x, y):
#     total = x + y

# print(add2(1, 2))  # using print() because `None` is not displayed by default

# Printing in a function displays the value to the user but it does not return the value:

# def add3(x, y):
#     total = x + y
#     print(total)

# x = add3(1, 2)  # 3 is printed, not assigned
# print(x)        # value is `None`

# When `return` is encountered in a function, the function exits immediately. 
# Thus you should be careful to ensure that every code path has exactly one return 
# statement. For example:

# def positive_or_negative(n):
#     if n < 0:
#         return 'negative'
#     elif n > 0:
#         return 'positive'

# print('-999 is', positive_or_negative(-999))
# print('50 is', positive_or_negative(50))
# print('0 is', positive_or_negative(0))

# Similarly, a `return` statement in a loop will only return the first value it 
# encounters. Consider these three versions of a function that returns the 3 
# highest values in a list:

# scores = [9, 2, 5, 3, 8, 5, 7]

# def top3_buggy(xs):
#     ranked = sorted(xs)
#     for x in ranked[-3:]:
#         return x

# def top3_ok(xs):
#     ranked = sorted(xs)
#     top = []
#     for x in ranked[-3:]:
#         top.append(x)
#     return top

# def top3_better(xs):
#     return sorted(xs)[-3:]

# print(top3_buggy(scores))
# print(top3_ok(scores))
# print(top3_better(scores))


# ## Modules
# Python 'modules' are files with a `.py` extension that contain Python code. 
# When you have imported things like `from nltk.book import *` there is a `book.py` 
# file in a `nltk/` directory that is loaded by Python. (If you are curious, 
# you can see `book.py` here: https://github.com/nltk/nltk/blob/develop/nltk/book.py)

# Modules, like functions, help with code reuse. Where functions allow you to 
# reuse code within a session (a Jupyter notebook, a script, etc.), modules allow 
# you to save and import code for use in multiple sessions. They also make it easy 
# for you to share code with others.

# Creating and using modules is easy, however it is not easy to create modules in 
# a Jupyter Notebook. Below I resort to some rather arcane measures to create a 
# temporary directory into which I write a `mymod.py` file, then make the directory 
# known to Python so it can be imported. You can safely ignore all the code I use 
# for this and focus on the middle part. It writes the contents of the module 
# (as a string) to the module file and then imports it.

# (Really just ignore the confusing part... Normally you create a module just by 
# saving a file using a text editor.)

# In order to write to a file, we need the Python code as a string:

# contents = '''
# def greet(name):
#     print('Hello, {}, from mymod.py!'.format(name))
    
# def add(x, y):
#     return x + y
# '''

# Now the following code writes it to a module file and imports it:

# # IGNORE THIS ##################################################
# import os
# import sys
# import tempfile

# module_dir = tempfile.TemporaryDirectory()
# sys.path.insert(0, module_dir.name)
# module_path = os.path.join(module_dir.name, 'mymod.py')

# with open(module_path, 'w') as fh:
#     fh.write(contents)

# ################################################################
# # THIS IS THE INTERESTING BIT ##################################

# # now we can import mymod
# import mymod
# mymod.greet('world')
# print(mymod.add(5, 9))
    
# # or we can import things from mymod
# from mymod import greet
# greet('again')
    
# ################################################################
# # OK NOW CAN LOOK AWAY AGAIN ###################################
    
# module_dir.cleanup()
# sys.path = sys.path[1:]
# del sys.modules['mymod']
# del mymod
# del greet

# We will look at modules more closely for the group project in the coming weeks.


# ## Conditional Frequency Distributions

# In previous weeks we used NLTK's `FreqDist` functionality, which takes a list 
# of things, counts how many times each item occurs, and makes a dictionary mapping 
# the items to their counts. This week we introduced the `nltk.ConditionalFreqDist` 
# which takes (condition, item) *pairs* of things and creates a `FreqDist` for all 
# items that share a condition. These are useful for creating and comparing word 
# frequencies across different genres or texts:

# import nltk
# from nltk.corpus import gutenberg

# # get some words to work with
# persuasion_words = gutenberg.words('austen-persuasion.txt')
# moby_dick_words = gutenberg.words('melville-moby_dick.txt')

# # pair each word in the books with the author's name
# austen = [('Austen', w) for w in persuasion_words]
# melville = [('Melville', w) for w in moby_dick_words]

# # concatenate these lists and create a ConditionalFreqDist
# cfd = nltk.ConditionalFreqDist(austen + melville)

# # print all the conditions:
# print(cfd.conditions())

# The resulting object contains the individual frequency distributions:
# cfd['Austen']
# cfd['Melville']

# But it also allows for comparison:
# cfd.tabulate(conditions=cfd.conditions(),
#              samples='can could may might must will'.split())

# `ConditionalFreqDist` is also useful for modeling relative bigram frequencies:
# bigrams = nltk.ConditionalFreqDist(nltk.bigrams(persuasion_words))

# Now there's lots of conditions:
# len(bigrams.conditions())

# What is the distribution of words that follow "persuade"?
# print(bigrams['persuade'])