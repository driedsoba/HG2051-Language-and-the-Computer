## Name: Liw Jun Le
## Matric number: U2221922D

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        start = "*** START OF THE PROJECT GUTENBERG EBOOK THE GREAT GATSBY ***"
        end = "*** END OF THE PROJECT GUTENBERG EBOOK THE GREAT GATSBY ***"
        text = text.split(start)[1].split(end)[0]
        return text

# Load your text
text =  read_file('text.txt')

# Tokenize the text
tokens = word_tokenize(text)

# Load NLTK's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')

# Remove non-alphabetic tokens and stopwords
tokens = [token for token in tokens if token.isalpha() and token.lower() not in stopwords]

# Tag the tokens
tagged = nltk.pos_tag(tokens)

# Filter out the nouns and verbs, excluding proper nouns
nouns = [(word, pos) for word, pos in tagged if pos in ['NN', 'NNS']] # common nouns singular and plural
verbs = [(word, pos) for word, pos in tagged if pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']] # various forms of verbs

# Create a frequency distribution of the nouns and verbs
fdist_nouns = FreqDist(nouns)
fdist_verbs = FreqDist(verbs)

# Extract the top 100 nouns and verbs
top_nouns = fdist_nouns.most_common(100)
top_verbs = fdist_verbs.most_common(100)

# Write the top 100 nouns and verbs to separate Excel files
df_nouns = pd.DataFrame(top_nouns, columns=['Noun_Type', 'Frequency'])
df_verbs = pd.DataFrame(top_verbs, columns=['Verb_Type', 'Frequency'])

# Split the 'Noun_Type' and 'Verb_Type' into two separate columns
df_nouns[['Noun', 'Type']] = pd.DataFrame(df_nouns['Noun_Type'].tolist(), index=df_nouns.index)
df_verbs[['Verb', 'Type']] = pd.DataFrame(df_verbs['Verb_Type'].tolist(), index=df_verbs.index)

# Drop the 'Noun_Type' and 'Verb_Type' columns
df_nouns = df_nouns.drop(['Noun_Type'], axis=1)
df_verbs = df_verbs.drop(['Verb_Type'], axis=1)

# Sort the DataFrames alphabetically by the 'Noun' and 'Verb' columns
df_nouns = df_nouns.sort_values(by='Noun')
df_verbs = df_verbs.sort_values(by='Verb')

df_nouns.to_excel('nouns.xlsx', index=False)
df_verbs.to_excel('verbs.xlsx', index=False)
