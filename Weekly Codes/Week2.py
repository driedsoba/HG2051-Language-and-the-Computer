# WEEK 2 PRACTICE

s = ('There are seven days, there are seven days, '
     'there are seven days in a week. '
     'Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday')

# How many times does the word “day” occur in the string?
print(s.count('day')) #10

# How many times do the tokens “day”, “days”, and “days,” (note the comma) occur in the list of tokens (use split())?
print(s.split().count('day')) #0
print(s.split().count('days')) #1
print(s.split().count('days,')) #2

# How many tokens are there in total?
print(len(s.split())) #22

# Find the relative frequency of the token “are” (number of times it occurs over the count of all tokens)
print(s.split().count('are') / 22) #0.13636363636363635

# What is the set of unique words?
print(set(s.split()))

# What is the set of unique letters?
import string
s1 = s.replace(' ', '') # remove spaces
s1 = s1.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
print(set(s1))