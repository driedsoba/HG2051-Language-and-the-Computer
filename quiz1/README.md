[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/_qEaipbw)
# HG2051 AY2023-24 (Sem 1) Midterm Quiz

This midterm quiz will allow you to practice what we have covered in the first
half of the course: using `list` and/or `dict` types, opening or writing to
files, using string formatting, and making use of resources found in the `nltk`
library, specifically WordNet.

For this task you will create a lexical resource from a book of your choice
taken from the Gutenberg corpus in the NLTK library. Expected output is given
further below.

You will have 1.5 to 2 hours to complete the quiz (by updating this repository).
The quiz is not autograded, but you are encouraged to write your own tests to
ensure that the goals are met. You are welcome to use online resources, but
keep in mind that the quiz will be monitored and collusion or cheating will
result in automatic failure.

## Instructions

Clone this repository on your local machine in order to edit the quiz script,
then follow the guidelines of the task. There is some basic code in `quiz1.py`
to get you started. Edit the `name` and `matric number` lines in the quiz code
before you begin.

### Getting started

This task requires you to have NLTK installed and the WordNet and Gutenberg
corpora downloaded.

### General Task

Choose a book from the NLTK Gutenberg corpus. Retrieve the top 100 non-stopwords
from the book, and use them as a basis for a human-readable dictionary.

Using the English WordNet, find part of speech, definitions, and examples for
each word. For the purpose of this quiz, the POS, def, example in the first
synset returned by wordnet is acceptable.

Write this dictionary to a `.txt` or (tab-delimited) `.csv` file. The file
should contain one line for each word, with the first item in the line being
the word, followed by the POS, def, and example.

#### Specific tasks

Organize the dictionary alphabetically.

Ensure the dictionary does not contain stopwords, names, or punctuation.

Define at least one function in your code. If you're having trouble doing so,
you may want to get your code working first, and then see which part of it you
could convert into a function.

#### Output

1. One `.txt` or `.csv` file containing 100 lines (words with POS, def, ex).
2. Python code to generate the output that contains comments describing how
the code operates. I should be able to run the code in the terminal and get
output as per #1. Your code should contain at least one defined function.
3. A written portion (a README.md, text file, or comments at the end of your
code) that lays out your thought process, concerns with the existing code, and
ways in which the dictionary could be improved.

***Bonus*** *To make this dictionary more easily readable, convert it into an
Excel spreadsheet using the `pandas` library, with headers for each of the
columns. Your output will therefore include an additional (`.xlsx`) file.*

### Submission

*IMPORTANT:* Ensure that your name and matric number are listed at the top of
your quiz script before submission.
