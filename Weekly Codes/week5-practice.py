# # Week 5
# import nltk  # make sure NLTK is installed and loaded
# ## Word Lists

# Use the `nltk.corpus.words` wordlist to estimate the following for several text corpora.
# nltk.download('words')
# nltk.download('gutenberg')
from nltk.corpus import words
from nltk.corpus import gutenberg 
# - Choose a variety of texts from the Gutenberg corpus. What percentage of the texts' vocabularies are not in the wordlist?
print(gutenberg.fileids())  # inspect available files
files = ['austen-emma.txt', 'milton-paradise.txt', 'shakespeare-macbeth.txt']  # choose some
WORDS = set(words.words())  # words.words() is a list; make it a set to speed up lookup

for file in files:
    # Get the list of words in the text and normalize early.
    # The isalpha() filter removes tokens like ",", but also valid words with punctuation.
    # How you normalize and filter is up to you.
    textwords = [w.lower() for w in gutenberg.words(file) if w.isalpha()]
    # Words not in the set of "known" words are often called OOV (out-of-vocabulary)
    oov = [w for w in textwords if w not in WORDS]
    print(file)
    print('  sample:', oov[:10])
    print('  percent of tokens that are unknown:', 100 * len(oov) / len(textwords))
    print('  percent of types that are unknown:', 100 * len(set(oov)) / len(set(textwords)))

# - What percentage of the wordlist are present in the texts?
for file in files:
    # Get the list of words, as before.
    textwords = [w.lower() for w in gutenberg.words(file) if w.isalpha()]
    # IV = in-vocabulary, by analogy to OOV
    iv = [w for w in textwords if w in WORDS]
    print(file)
    print('  percent of wordlist present in text:', 100 * len(set(iv)) / len(WORDS))

# ## CMU Pronouncing Dictionary
# Use the ARPABET transcriptions in the `nltk.corpus.cmudict` corpus to investigate sound patterns.
# nltk.download('cmudict')
from nltk.corpus import cmudict
cmu = cmudict.dict()
print(cmu['pronounce'])

# - Pick some minimal pairs and look at vowel differences (e.g., *pick* / *pack* / *peck* / *peak*)
for word in ('pick', 'pack', 'peck', 'peak'):
    print(word, '->', cmu[word])

# - Devise a function for identifying rhyming words (how they are identified is up to you)
def rhymes(word1, word2):
    pron_list1 = cmu[word1]
    pron_list2 = cmu[word2]
    return any(p1[-2:] == p2[-2:]  # are the last 2 phonemes enough? are they too much?
               for p1 in pron_list1
               for p2 in pron_list2)

print('rhymes with "pack":')

for other in ('pick', 'peck', 'peak', 'back', 'track'):
    print('  ', other, rhymes('pack', other))

# * (extra) why doesn't something like "smokestack" or "quarterback" rhyme with "pack" according to the function above?
#   - *smokestack* and *quarterback* have three syllables, while *pack* has only one
#   - *smokestack* and *quarterback* have stress on the first syllable, while *pack* has stress on the second syllable
#   - *smokestack* and *quarterback* have a different vowel in the first syllable than *pack*
for word in ('pack', 'smokestack', 'quarterback'):
    print(word, cmu[word])

# - What are the largest clusters of rhyming words?
# first create a structure mapping each rhyming scheme to the list of words ending in the scheme
clusters = {}
for word, pron_list in cmu.items():
    for pron in pron_list:
        scheme = tuple(pron[-2:])  # make it a tuple so it can be a dictionary key
        # initialize an empty list if we haven't seem the rhyming scheme before
        if scheme not in clusters:
            clusters[scheme] = []
        clusters[scheme].append(word)

# # To find the largets cluster, we could go through each and keep track of the largest we've seen:
max_scheme = None
max_value = 0
for scheme, cluster in clusters.items():
    if len(cluster) > max_value:
        max_scheme = scheme
        max_value = len(cluster)
print('largest cluster')
print('  scheme:', max_scheme)
print('  size:', len(clusters[max_scheme]))

# Alternatively, use the max() function with a "lambda" expression (like an inline function)
max_scheme = max(clusters, key=lambda scheme: len(clusters[scheme]))
print('largest cluster')
print('  scheme:', max_scheme)
print('  size:', len(clusters[max_scheme]))

print('sample:', clusters[max_scheme][:10])

# ## WordNet
# Use `nltk.corpus.wordnet` to look at word relations.
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn

# - What are the synsets of *student*?
print(wn.synsets('student'))

# - What is the definition of each synset of student?
for synset in wn.synsets('student'):
    print(synset, synset.definition())

# - What are the **hyponyms** of each synset of *student*?
for synset in wn.synsets('student'):
    print(synset, synset.hyponyms())
    print()  # a blank line in between helps; these are long lists

# - How many synsets are avaiable for each of *professor*, *lecturer*, *instructor*, and *teacher*?
words = ('professor', 'lecturer', 'instructor', 'teacher')
for word in words:
    print(word, len(wn.synsets(word)))

# - Are there any overlapping synsets among them?
# the direction of the pairing (e.g., ('professor', 'lecturer') or ('lecturer', 'professor')
# doesn't matter, so we'll avoid that with a slice in the second for-loop)
for i, word1 in enumerate(words):
    for word2 in words[i+1:]:
        print(word1, word2, set(wn.synsets(word1)).intersection(wn.synsets(word2)))

# - Use the `lowest_common_hypernyms()` method on synsets to find what is the shared
#  **hypernym** of *student* and *professor*. How about *professor* and *lecturer*?
# for this I'll pick 'student.n.01' and 'professor.n.01'
st_pr = wn.synset('student.n.01').lowest_common_hypernyms(wn.synset('professor.n.01'))
print(st_pr)
# for this I'll pick 'professor.n.01' and 'lector.n.02'
pr_lec = wn.synset('professor.n.01').lowest_common_hypernyms(wn.synset('lector.n.02'))
print(pr_lec)

# - The synsets retrieved from WordNet are generally sorted by the frequency of occurrence
# (bonus question: how would the "frequency of occurrence" be computed?). Write a function
# that tags each word in a sentence with the first synset returned by WordNet. Skip words
# that do not return any synsets.

from nltk.tokenize import word_tokenize
def syn_tag(sentence):
    # split the sentence into words
    words = word_tokenize(sentence)
    # for each word, get the synsets
    for word in words:
        synsets = wn.synsets(word)
        # if there are synsets, print the first one
        if synsets:
            print(word, synsets[0])

# For bonus question: we need a corpus that has been annotated with word senses
# to determine frequency *for that corpus*. The creators of the wordnet can also
# order the synsets to encode general preference.

def sense_tag(sentence):
    # split the sentence into words
    words = word_tokenize(sentence)
    # for each word, get the synsets
    for word in words:
        synsets = wn.synsets(word)
        # if there are synsets, print the first one
        if synsets:
            print(word, synsets[0])
        else:
            print(word, None)

# Consider these sentences:
#   - *The doctor is in, today.*
#   - *The doctor is in the office, today.*
#   - *The doctor's shoes are very in, this season.*

# **Q:** With your sysent tagger, do all sentences get the same synset for *in*?
# Which sysnets should they get?
print(sense_tag('The doctor is in , today .'))  # spaces around punctuation because my tokenization is just split()
print(sense_tag('The doctor is in the office, today .'))
print(sense_tag("The doctor's shoes are very in , this season ."))
for synset in wn.synsets('in'):
    print(synset, synset.definition())

# They all get the same but it's not correct for any. They should get:
# - in.s.01
# - None
# - in.s.03

# **Q:** Can you think of ways we might improve the tagger to get better performance?

# **A:** If we had the part-of-speech information for each word, this could help
#  wordnet choose the correct synset more often. We could also try to build
#  statistical models, for instance by looking at each word's left and right
#  context to help decide, but this requires annotated data to train the model.

# **Q:** How would we measure if the performance improves or degrades?

# **A:** We need some **gold standard** annotations to compare against. Without those,
#  we would have to manually determine, with our own intuition, whether an annotation
#  is correct or not, and this has issues with consistency and scale.
