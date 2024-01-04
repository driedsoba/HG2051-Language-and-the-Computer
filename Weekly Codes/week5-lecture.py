# # Week 05

# Overview

# * [**Python Recap**](#Python-Recap)
#   - basic types: `str`, `int`, `float`
#   - common constant values: `True`, `False`, and `None`
#   - basic data structures: `list`, `set`, `tuple`, `dict`
#   - list, set, and dict comprehensions (e.g., `[1/x for x in range(-10,10) if x != 0]`)
#   - control structures (`if`, `for`, `while`)
#   - string formatting
#   - functions
#   - modules
#   - built-in functions: print(), range(), len(), min(), max(), 
#     sum(), zip(), reversed(), sort(), all(), any(), list(), 
#     set(), dict(), tuple(), dir(), help())
# * **NLTK Topics**
#   * [**Lexicons**](#Lexicons)

#   * [**WordNet**](#WordNet)
# ## Python Recap

# So far we have established a good base of basic Python, such as how to create 
# and use the basic `str`, `int`, and `float` types:

name = 'Alex'  # string (str)
age = 20       # integer (int)
gpa = 3.9      # floating point number (float)

# How to compose them into larger structures, such as `list`, `set`, `dict`, and `tuple`:
alex = (name, age, gpa)                                      # tuple
students = [alex, ('Billy', 21, 3.5), ('Charlie', 19, 4.0)]  # list
names = {student[0] for student in students}                 # set, set-comprehension
age_map = {name: age for name, age, gpa in students}         # dict, dict-comprehension

# How to test for truth and use control structures:
for name, age, gpa in students:    # for loop
    if gpa >= 4.0:                 # if statement
        print('{0} (age {1}) has a perfect grade point average'
              .format(name, age))  # string formatting
        
# How to create and call functions:
def repeat(x, n):  # Define a function
    """Return a list of *x* repeated *n* times."""
    return [x] * n

rep = repeat('abc', 3)   # Call the function
print(rep)

# How to create and import modules (files with a `.py` extension containing Python
# code). E.g.,

# my_mod.py
def say_hello():
    print('Hello from my_module')

# then...

# >>> from my_mod import say_hello  # import say_hello() from my_mod
# >>> say_hello()
# 'Hello from my_module'

# And how to use some built-in functions (https://docs.python.org/3/library/functions.html).
# In the linked image below, we have learned those highlighted in yellow and have
# mentioned those in green. Those in white are functions I have used in my 10 years
# of programming, while the remainder I have never used (people in other fields may
# use different subsets of functions):

# https://hg2051-ntu.github.io/static/Python-built-in-functions-highlighted.png

## Lexicons

# Lexicons are "lexical resources", which provide information about words.
# Dictionaries (not the Python kind) and thesauri are lexical resources, as
# are simple lists of words where the inclusion of the word in the list is
# the encoded information.

# Consider an English dictionary entry: https://www.collinsdictionary.com/dictionary/english/word_1
# (Collins Dictionary)
# * **Q:** What kinds of information are presented?
# * **A:** pronunciation, etymology, synonyms and antonyms, definitions, senses, etc.

# A lexicon contrasts with a text in that the lexicon *describes* words
# while the text *uses* words. Consider:

import nltk
from nltk.corpus import gutenberg

sents = gutenberg.sents('blake-poems.txt')  # is this a lexicon or text? lexicon
print(sents)
words = gutenberg.words('blake-poems.txt')  # is this? text.
text = nltk.Text(words)                     # is this? lexicon.
freq = nltk.FreqDist(words)                 # is this? lexicon.
vocab = set(words)                          # or even this? lexicon.

# * **Q:** Which of the above are lexical resources, which are texts?
# * **A:** `sents`, `words`, and `text` are texts as they *use* lexical
# content, e.g., to tell a story. `freq` and `vocab` are lexical resources
# because they *describe* the words (their frequency and presence in the
# corpus, respectively).

# These lexical resources are simple ones relevant for a single document,
# but more useful lexical resources are hand-curated or are composed from
# multiple sources.

### Wordlist resources
# The following are some lexicons in the NLTK that are simple word lists:
english_words = nltk.corpus.words.words()                     # English words from a spelling dictionary
english_stopwords = nltk.corpus.stopwords.words()             # English words common to all domains
english_female_names = nltk.corpus.names.words('female.txt')  # Collection of female names in English
english_male_names = nltk.corpus.names.words('male.txt')      # Collection of male names in English

# * **Q:** What are some things that can you do with these simple word lists?
# * **A:** filter out stopwords, check spelling, look at spelling
# differences between male and female names, find which names are unisex, etc.

### Wordmap resources
# Word maps pair a word with other information about the word:
from nltk.corpus import cmudict
entries = cmudict.entries()
mapping = cmudict.dict()
print(mapping['chicago'])

# * **Q:** What kinds of things can you do with a pronunciation dictionary?
# * **A:** Find rhyming words, find proportion of words whose pronunciation
#  closely aligns with its orthography, assist a text-to-speech system, etc.

### Comparative wordlist resources

# "Comparative wordlists" are multiple lists of words that pair up with other
# lists that differ on some dimension. The NLTK has "Swadesh lists" where each
# word has (basically) the same meaning as the corresponding word in another
# list, but in a different language.
from nltk.corpus import swadesh
en2pt = swadesh.entries(['en', 'pt'])  # english to portuguese
en2pt[:5]

# * **Q:** What kinds of things can you do with Swadesh lists?
# * **A:** translate words, comparative linguistics, etc.

## Lexicon Exercises
#### 1a. Find the 50 most frequent words (see Week 2) in Jane Austen's Emma.
from nltk.corpus import gutenberg
words = gutenberg.words('austen-emma.txt')
import nltk
fd = nltk.FreqDist(words)
fd.most_common(50)

#### 1b. Then find the 50 most frequent words that are not stopwords. 
from nltk.corpus import stopwords
stoplist = stopwords.words('english')
emma_nostop = [word for word in words if word not in stoplist]
fd2 = nltk.FreqDist(emma_nostop)
print(fd2.most_common(50))
#### 2a. What proportion of entries in the CMU Pronuncation Dictionary
# have the same initial phoneme code as their first letter?
from nltk.corpus import cmudict
cmu = cmudict.entries()
wordlist = []
for word, pron in cmu:
    if word[0] == pron[0].lower():
        wordlist.append(word)
len(wordlist)/len(cmu) * 100
#### 2b. What are common mismatches?
pairs = []
for word, pron in cmu:
    if word[0] != pron[0].lower():  # also try pron[0][0].lower()
        pairs.append((word[0], pron[0]))
fd3 = nltk.FreqDist(pairs)
fd3.most_common(50)

## WordNet (series of semantic relations for English)) 

from nltk.corpus import wordnet as wn  # Q: what does "as wn" do here?
word_ss = wn.synsets('word')
print(word_ss)
word_ss[4].lemma_names()
word_ss[4].definition()
word_ss[4].examples()
word_ss[4].hypernyms()
word_ss[4].hyponyms()
wn.synsets('room')[0].part_meronyms()
wn.synsets('room')[0].part_holonyms()
wn.synsets('water')[0].substance_meronyms()
wn.synsets('water')[0].substance_holonyms()

## WordNet Exercises

# Open the [Open Multilingual Wordnet interface](https://compling.upol.cz/ntumc/cgi-bin/wn-gridx.cgi?gridmode=grid)

# * Find hyponyms of "student". What kind of student are you?
# * Compare hypernyms of "student" and "professor". What's the difference?
# * Compare hyponyms of "professor" and "lecturer". Is WordNet US English?
# * Adjectives: Compare "big", "large", "great". What are their antonyms?
# * Multiword Expressions (Collocations): An MWE like "big sister" has its
#   own WordNet entry. Which combinations of "big/large/great sister/uncle/toe"
#   are listed in WordNet?

# * Load wordnet inside python.
from nltk.corpus import wordnet as wn
#   - Look at the different synsets for *bird*.
#   - How many are there?

bird=wn.synsets('bird')

len(bird)
#   - What are their definitions?
for synset in bird:
    print('{!r}: {}\n    {}'.format(
        synset,
        ', '.join(synset.lemma_names()),
        synset.definition()))
#   - How deep in the hierarchy are they?
for synset in bird:
    dist = max(dist for _, dist in synset.hypernym_distances())
    print(synset, 'is {} levels deep'.format(dist))
#   - For the first synset (`bird.n.01`) print the lemmas in the languages other than English (skipped in class; you can try if you install 'omw' from `nltk.download()`)
nltk.download('omw')  # if necessary
nltk.download("wordnet")
nltk.download("omw-1.4")
# if you want the wiktionary data
nltk.download("extended_omw")

ayam=wn.synsets('ayam', lang='ind') # need to know the word and the language, different from swadesh
print(ayam) # can provide the synset of english word

# wnlangs = ['aar', 'afr', 'aka', 'als', 'amh', 'arb', 'asm', 'aze', 'bam', 'bel', 'ben', 'bod', 'bos', 'bre', 'bul', 'cat', 'ces', 'cmn', 'cor', 'cym', 'dan', 'deu', 'dzo', 'ell', 'eng', 'epo', 'est', 'eus', 'ewe', 'fao', 'fas', 'fin', 'fra', 'ful', 'gla', 'gle', 'glg', 'glv', 'guj', 'hau', 'heb', 'hin', 'hrv', 'hun', 'hye', 'ibo', 'iii', 'ina', 'ind', 'isl', 'ita', 'jpn', 'kal', 'kan', 'kat', 'kaz', 'khm', 'kik', 'kin', 'kir', 'kor', 'lao', 'lav', 'lin', 'lit', 'lub', 'lug', 'mal', 'mar', 'mkd', 'mlg', 'mlt', 'mon', 'mya', 'nbl', 'nde', 'nep', 'nld', 'nno', 'nob', 'oci', 'ori', 'orm', 'pan', 'pol', 'por', 'pus', 'roh', 'ron', 'run', 'rus', 'sag', 'sin', 'slk', 'slv', 'sme', 'sna', 'som', 'sot', 'spa', 'srp', 'ssw', 'swa', 'swe', 'tam', 'tel', 'tgk', 'tha', 'tir', 'ton', 'tsn', 'tso', 'tur', 'ukr', 'urd', 'uzb', 'ven', 'vie', 'xho', 'yor', 'zsm', 'zul']

wnlangs = ['als', 'arb', 'bul', 'cat', 'cmn', 'dan', 'ell', 'eus', 'fas', 'fin', 'fra', 'glg', 'heb', 'hrv', 'ind', 'ita', 'jpn', 'nld', 'nno', 'nob', 'pol', 'por', 'qcn', 'slv', 'spa', 'swe', 'tha', 'zsm']

for lg in wnlangs:
    if lg == 'eng':
        continue
    try:
        lemmas = wn.synset('bird.n.01').lemmas(lang=lg)
        print(lg, ':', ', '.join(lemma.name() for lemma in lemmas))
    except:
        pass
        # print(lg)

# - For each synset, print out each lemma and its frequency (hint freqency of a lemma is given by `lemma.count`)
for ss in bird:
    print(ss)
    for lemma in ss.lemmas():
        print('  ', lemma.name(), lemma.count())

# - Give the total frequency for each synset (skipped in class)
for ss in bird:
    freq = sum(lem.count() for lem in ss.lemmas())
    print(ss, ':', freq)
