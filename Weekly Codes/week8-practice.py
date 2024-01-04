# # Week 8

# Regular expressions, stemming, lemmatization, and segmentation.

# # Regex Basics

# First import the `re` library:
import re
# Then use `re.match()` to match the following strings:
re.match(r'a', 'a') # a single 'a'
re.match(r'a+', 'aaaaaaaa')  # multiple 'a's
re.match(r'[a-z]*', 'abcdefghijklmnopqrstuvwxyz')  # any letter
re.match(r'\w*', 'abcdefghijklmnopqrstuvwxyz')  # any letter (alternative)
re.match(r'[A-Ca-c]*', 'AaBbCc')  # upper and lower-case letters
re.match(r'\w+', 'Aあ啊')  # all word characters (hint, use a character class)

# ## Searching

# Now use `re.search()` to find a match while ignoring false matches
# # match the article 'a' but not other 'a's
for s in ('Apples are a fruit', 'An apple each day', 'A pear is not an apple'):
    print(list(re.finditer(r'\b([Aa]n?|[Tt]he)\b', s)))

# Use `re.findall()` over the text of Jane Austen's *Sense and Sensibility* to find hyphenated words:
import nltk
sense = nltk.corpus.gutenberg.raw('austen-sense.txt')
set(re.findall(r'\w+(?:-\w+)+', sense))

# ## Substitution

# Now detect -y words inflected as -ies (e.g., *fly* -> *flies*). Save them to a set called `ies`.
ies = set(re.findall(r'(?:\w+-)*\w+ies\b', sense))
print(ies)

# Use `re.sub()` to try and deinflect them to their dictionary form, and check if they are in the dictionary.
WORDS = nltk.corpus.words.words()
for word in ies:
    y = re.sub(r'ies$', r'y', word)
    if y.lower() in WORDS:
        print('YES', word)
    else:
        print('NO ', word)

# # Stemming and Lemmatization

# Above the `re.sub()` call replaced `ies` with `y`, and this is a crude form of lemmatization. Stemming is if we removed the `ies` but did not insert anything. Stemming is more robust to novel or mispelled words, but lemmatization gives cleaner results (when it works). In the NLTK, you may notice that the WordNet module can do some lemmatization. For instance, it can find synsets for *catch* when queried with *caught*:
from nltk.corpus import wordnet as wn
print(wn.synsets('caught'))

# This works by applying some basic morphological processing (like our 'ies' -> 'y' substitution) and looking if the result exists in WordNet. WordNet also contains some irregular forms, which is how it finds 'catch' for 'caught'. You can make use of WordNet's lemmatizer without using WordNet itself (but note it only works for English):
from nltk.stem.wordnet import WordNetLemmatizer
wnl = WordNetLemmatizer()
print(wnl.lemmatize('caught', pos='v'))

# But note that the default part-of-speech is 'n' (noun):
print(help(wnl.lemmatize))
# So it won't work well on verbs if the part-of-speech is not specified, 
# or in geneneral when the part-of-speech is incorrect:
# wnl.lemmatize('caught')  # pos='n' is the default
# wnl.lemmatize('oxen')  # default works well for nouns
# wnl.lemmatize('oxen', pos='v')  # specifying the wrong pos is also bad