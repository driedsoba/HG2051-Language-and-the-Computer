# # Week 10

# This week covers part of speech tagging in more detail.

# Overview
# * Tagging and Tagsets
# * Heuristic-based Tagging
# * N-Gram Tagging
# * Visualizing Errors
# * State-of-the-art Taggers

# First import some things to work with

import nltk
from nltk.corpus import brown
# nltk.download('brown')
# nltk.download('punkt')

brown_tagged_news = brown.tagged_sents(categories='news')
brown_news = brown.sents(categories='news')
brown_tagged_scifi = brown.tagged_sents(categories='science_fiction')
brown_scifi = brown.sents(categories='science_fiction')

sent = nltk.word_tokenize('From each according to their ability, to each according to their need.')
print(sent)

# # Tagging and Tagsets

# Recall that part-of-speech tagging assigns a word category to each token in a sentence:
# nltk.pos_tag(sent)
# The categories are defined by **tagsets**. The example above uses the English Penn Treebank tagset, but others are available, even cross-lingual sets. Part-of-speech tagging isn't just for words, but also punctuation and sometimes parts of words. For example, the [Mecab](https://taku910.github.io/mecab/) morphological analyzer for Japanese does both word segmentation and tagging, and morphological segments get their own tag (note: this is shown executed in a terminal, not Python):

# $ mecab -Osimple <<< "能力に応じて働き、必要に応じて受け取る。"
# 能力	名詞-一般
# に	助詞-格助詞-一般
# 応じ	動詞-自立
# て	助詞-接続助詞
# 働き	動詞-自立
# 、	記号-読点
# 必要	名詞-形容動詞語幹
# に	助詞-副詞化
# 応じ	動詞-自立
# て	助詞-接続助詞
# 受け取る	動詞-自立
# 。	記号-句点
# EOS

## Heuristic-based Tagging
# A simple way to tag is to use basic statistics or language knowledge to 
# create a tagger with hand-built rules.

### Default Tagger
# The default tagger assigns the same tag to all tokens. This is useless 
# for general purpose uses, but it is useful for establishing baseline performance.
nn_tagger = nltk.DefaultTagger('NN')
nn_tagger.tag(sent)
nn_tagger.accuracy(brown_tagged_news)
nn_tagger.accuracy(brown_tagged_scifi)

# Why choose `NN`?
fd = nltk.FreqDist(tag for sent in brown_tagged_news for _, tag in sent)
print(fd.most_common(20))

#### TODO: try using a different default tag and evaluate it
nn_tagger = nltk.DefaultTagger('VBN')
print(nn_tagger.tag(sent))
print("Default tagger acc on Brown News:", nn_tagger.accuracy(brown_tagged_news))

## Pattern-based Tagging
# With a bit more information about the forms of the words, the tagger can do better:
regexp_tagger2 = nltk.RegexpTagger(
    [(r'^\.$', '.'),
    #  (r'^,$', ','),
    #  (r'.*ful$', 'JJ'),
    #  (r'^un', 'JJ'),
    #  (r'.*ly$', 'RB'),
     (r'.*ing$', 'VBG'),                # gerunds
     (r'.*ed$', 'VBD'),                 # simple past
     (r'.*es$', 'VBZ'),                 # 3rd singular present
     (r'.*ould$', 'MD'),                # modals
     (r'.*\'s$', 'NN$'),                # possessive nouns
     (r'.*s$', 'NNS'),                  # plural nouns
     (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'),  # cardinal numbers
     (r'.*', 'NN')                      # nouns (default)
    ])
print(regexp_tagger2.tag(sent))
print("RegEx tagger2 acc on Brown News:", regexp_tagger2.accuracy(brown_tagged_news))
print("RegEx tagger2 acc on Brown SciFi:", regexp_tagger2.accuracy(brown_tagged_scifi))

#### TODO: try adding some more rules, or rearranging them, to improve performance
regexp_tagger = nltk.RegexpTagger(
    [(r'.*ing$', 'VBG'),                # gerunds
     (r'.*ed$', 'VBD'),                 # simple past
     (r'.*es$', 'VBZ'),                 # 3rd singular present
     (r'.*ould$', 'MD'),                # modals
     (r'.*\'s$', 'NN$'),                # possessive nouns
     (r'.*s$', 'NNS'),                  # plural nouns
     (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'),  # cardinal numbers
     (r'.*', 'NN')                      # nouns (default)
    ])
print(regexp_tagger.tag(sent))
print("RegEx tagger acc on Brown News:", regexp_tagger.accuracy(brown_tagged_news))
print("RegEx tagger acc on Brown SciFi:", regexp_tagger.accuracy(brown_tagged_scifi))

## N-Gram Tagging
# Rather than trying to hand-build many rules to cover all of a language, 
# we can **train** a tagger to **learn** the best tags for each word. This 
# uses statistical inference based on hand-tagged (gold) data, which we 
# assume is correct.

### Unigram Tagging
# First we will start by assigning the tag most frequently associated with 
# a particular word form for the 100 most frequent words (all other words 
# get a tag of `None`):

### TODO: find the N most frequent words in the Brown corpus's "news" category 
N = 100

### TODO: find the most likely tags for those words (create a dict mapping {word: tag})
model = {}

### TODO: build a UnigramTagger using the most likely tags (the dict you built) as a model
baseline_tagger = nltk.UnigramTagger(model=model)

### TODO: evaluate this tagger on the news and scifi data
print(baseline_tagger.accuracy(brown_tagged_news))

### TODO: increase `N`, then retrain, then re-evaluate
N = 100000
model = {}

baseline_tagger = nltk.UnigramTagger(model=model)
print(baseline_tagger.accuracy(brown_tagged_news))
unitagger = nltk.UnigramTagger(brown_tagged_news)
print(unitagger.accuracy(brown_tagged_news))

### Bigram and Trigram Tagging
# Now let's give the model a bit of context by using bigrams.
bigram_tagger = nltk.BigramTagger(brown_tagged_news)
print(bigram_tagger.tag(sent))
print("Bigram acc on Brown News:", bigram_tagger.accuracy(brown_tagged_news))
print("Bigram acc on Brown SciFi:", bigram_tagger.accuracy(brown_tagged_scifi))

trigram_tagger = nltk.TrigramTagger(brown_tagged_news)
print("Trigram acc on Brown News:", trigram_tagger.accuracy(brown_tagged_news))

# Did the accuracy go up with more n-grams? Try using a backoff and try again:
bigram_tagger = nltk.BigramTagger(brown_tagged_news, backoff=unitagger)
print("Bigram acc on Brown News:", bigram_tagger.accuracy(brown_tagged_news))
trigram_tagger = nltk.TrigramTagger(brown_tagged_news, backoff=bigram_tagger)
print("Trigram acc on Brown News:", trigram_tagger.accuracy(brown_tagged_news))
print("Trigram acc on Brown SciFi:", trigram_tagger.accuracy(brown_tagged_scifi))

# ## K-fold Cross-validation real world situations
# Split the training data (`brown_tagged_news` or `brown_tagged_scifi`) for 
# k-fold cross validation. For some value `k` (say, 5), set aside `1/k` for 
# test data and the remainder for training data. Train a bigram tagger with 
# backoff on the training data, then evaluate on the test data.

#  12345                       25
# |.....|.....|.....|.....|.....|

# i = 0
# test = [0:5]
# train = [5:len(data)]

# i = 1
# test = [5:10]
# train = [0:5] + [10:len(data)]

news = brown_tagged_news
print(924 * 5)

print(len(news))
k = 5
index = int( (1/k) * len(brown_tagged_news) )
accs = []

for i in range(k):
    # TODO: extract 1/k of the data for testing
    # TODO: extract (k-1)/k of the data for training
    # (hint, use 'index' and 'i' to find where to split)
    test_data = news[i*index:(i+1)*index] 
    train_data = news[:i*index] + news[(i+1)*index:]

#   # TODO: create a bigram tagger that backs off to a unigram tagger
#   # trained using the extracted training data
    unigram_tagger = nltk.unigram_tagger(train_data, backoff = nltk.DefaultTagger('NN'))
    bigram_tagger = nltk.bigram_tagger(train_data, backoff = unigram_tagger)
    # TODO: now evaluate on the test data
    acc = bigram_tagger.accuracy(test_data)
    print(f'i={i}, accuracy={acc}')
    accs.append(acc)
    print('average accuracy', sum(accs)/k)  # print the average

## Visualizing Errors
auto_tagged = bigram_tagger.tag(brown.words(categories='news'))
hand_tagged = brown.tagged_words(categories='news')
assert len(auto_tagged) == len(hand_tagged)

import matplotlib.pyplot as plt

t2t_cfd = nltk.ConditionalFreqDist(
    (t1[1], t2[1])
    for t1, t2 in zip(auto_tagged, hand_tagged)
    if t1[1] != t2[1])
t2t_cfd['NN'].plot()
plt.show()

## State-of-the-art Taggers
# The http://nlpprogress.com/ website tracks the start-of-the-art (SOTA) 
# performance of many different NLP tasks. For part of speech tagging 
# (http://nlpprogress.com/english/part-of-speech_tagging.html), the top 
# systems get over 97% accuracy. 
