# Quiz 2: Analysis of "The Great Gatsby"

## Process
1. **Text Preparation**: The text of "The Great Gatsby" was read from `text.txt`, removing Project Gutenberg's front and back matter as they would create noise in the frequency distrbution.
2. **Tokenization and Cleaning**: NLTK's `word_tokenize` was used to split the text into tokens. Non-alphabetic tokens, stopwords, and proper nouns were removed 
3. **Part of Speech Tagging**: NLTK's `pos_tag` function to tag each token with its corresponding part of speech.
4. **Frequency Analysis**: Separated nouns and verbs from the tagged tokens and calculated their frequencies.
5. **Output**: The top 100 nouns and verbs were sorted alphabetically and written to `nouns.xlsx` and `verbs.xlsx`, along with their frequencies and types.

## Outcomes
The outcome of this process is two Excel files:
- `nouns.xlsx`: Contains the top 100 nouns, sorted alphabetically, with frequency and type.
- `verbs.xlsx`: Contains the top 100 verbs, similarly sorted with frequency and type.

## Limitations
- **Removal of Names**: I thought of two approaches I could go with to remove names, either the more aggressive method of filtering out all capitalised words or relying on NLTK's POS tagger. I chose the latter as I felt that straight up filtering all capitalised words would cause a greater impact to the frequency distribution.

- **Reliability of NLTK's POS tagging**: The pos tagger does not take into account the context of the word that it is classifying and it is using capitalization as a clue to determine whether a word is a proper noun. This means that there could be instances of words that are common nouns being filtered out or even proper nouns that are not capitalised being missed out.


## References
- **The Great Gatsby Word Cloud** : https://kfronh1.github.io/Personal-Webpage/posts/2021-03-14-great-gatsby-word-cloud/

- **Pos Taggers** : https://devopedia.org/part-of-speech-tagging#:~:text=These%20tags%20then%20become%20useful,meanings%20and%20therefore%20multiple%20POS%20.
