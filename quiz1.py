## Name: Liw Jun Le
## Matric number: U2221922D

import nltk
from nltk.corpus import gutenberg, wordnet, stopwords
import string
import re
import pandas as pd

## Define variables
book = gutenberg.words('austen-emma.txt') # get the words in a book
stopwords_eng = set(stopwords.words('english')) # get the English stopwords
names_eng = set(nltk.corpus.names.words()) # get the English names
punctuations = set(string.punctuation) # get the English punctuations

## Create a new corpus without stopwords, names, symbols, and numbers
new_corpus = []
for word in book:
    # check if the word is not a stopword, name, symbol, or number
    if (word.lower() not in stopwords_eng and 
        word.lower() not in names_eng and 
        not re.match(r'^[\W_]+$', word) and
        not word.isdigit()):
        new_corpus.append(word.lower())

## Get the top 100 words
fdist = nltk.FreqDist(new_corpus)
top_words = [word for word, freq in fdist.most_common(100)]

## Create a dictionary with part of speech, definition, and example
## Addresses scenarios when part of speech, definition, or example is not available
word_dict = {}
for word in top_words:
    try:
        synsets = wordnet.synsets(word)
        if synsets:
            synset = synsets[0]
            # get the part of speech of the word
            pos = synset.pos() if synset.pos() else "No part of speech available"
            # get the definition of the word
            definition = synset.definition() if synset.definition() else "No definition available"
            # get the example of the word
            example = synset.examples()[0] if synset.examples() else "No example available"
            word_dict[word] = (pos, definition, example)
        else:
            word_dict[word] = ("No part of speech available", "No definition available", "No example available")
    except:
        pass

## Sort the words alphabetically
sorted_words = sorted(word_dict.keys())

## Write the dictionary to a file
with open("my_dictionary.txt", "w") as f:
    for word in sorted_words:
        pos, definition, example = word_dict[word]
        f.write(word + "\t" + pos + "\t" + definition + "\t" + example + "\n")

## Read the dictionary file
df = pd.read_csv("my_dictionary.txt", sep="\t", header=None)

## Add headers to the columns
df.columns = ["Word", "Part of Speech", "Definition", "Example"]

## Write the dataframe to an excel file
df.to_excel("my_dictionary.xlsx", index=False)


## A written portion (a README.md, text file, or comments at the end of your code) 
## that lays out your thought process, concerns with the existing code, and ways in 
## which the dictionary could be improved. 

## THOUGHT PROCESS
# I created a list object to store words which I filtered out from the book, initially I saw symbols
# and numbers not being filtered from the text file so I added a regular expression them out.
# Next I created a frequency distribution to get the top 100 words.
# With this frequency distribution, I used the words as key and tagged them with the values of part of speech, definition, and example.
# This was the hardest part of the quiz as I had to think of the possible cases where the part of speech, definition, or example was not available
# until I could get the total of the top 100 words written onto the text file, there were a quite a bit of trial and error to hit 100 words.
# Lastly, I wrote the dictionary to a text file and also the excel file.

## IMPROVEMENTS
# I think the dictionary could be improved by adding more information such as synonyms, antonyms, and hypernyms 
# because it shows the user words that have similar, opposite and more general representations respectively.
# An example of how it could be added is by using the synset object and calling the methods synonyms(), antonyms(), and hypernyms() respectively.
# In this quiz's context the synset object is synset = synsets[0] and the methods would be synset.synonyms(), synset.antonyms(), and synset.hypernyms().
# Additionally I think instead of just having the top 100 words, we could instead try having all the unique words in the book and sort them
# based on the magnitude of their term frequency, this would allow us to not only see how words can be used it also tells us how important the
# word is in the book where it is calculated by (number
# of times term appears in book / total number of terms in book).

# CONCERNS WITH EXISTING CODE
# From the code point of view, the code writes the dictionary to a file using a tab-separated format, 
# this means that it does not handle cases where the word or definition contains a tab character.
# This might cause issues when reading the file later.
# I would also think that having a consistent formatting is important for the text file, maybe it could be done
# by using dataframes from pandas to format it before writing it to the text file.