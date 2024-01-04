[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/1-EENyrH)
# HG2051 (AY23/24) Project 1: Individual assignment

## Project Setup

To set up this project, follow the steps below:

1. Install the required packages by running the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```

2. After installing the packages, download the necessary spaCy language model with the following command:
   ```bash
   python -m spacy download fr_core_news_sm
   ```

## Introduction

This project constitutes 30% of your final grade for HG2051. Please work on the
final program and report individually. Your code will be assessed based on its
functionality and simplicity/efficiency.

- The goal of this assignment is to demonstrate your programming and reasoning
abilities by working on a problem individually. If you have an idea for another
project that you would like to do instead, talk to me for approval.

- This project involves sorting and developing lexical resources for multiple languages.
Submission requirements include your data, output, and annotated code along
with a short writeup describing your goals, process, and results.

## Project 1: Machine translation

Machine translation involves automatically translating from one language to
another. While automated translation systems have increased in complexity in
recent years, you will be creating and evaluating a simple Python tool, using
a bilingual dictionary to translate text from one language to another.

The `project1.py` script in this repository has some basic code and example
files to get you started. Keep in mind that the basic code provides one
direction out of many possible directions you can take in developing your
program/solution. Your final submitted repository should not have any of the
example code or example texts in it.

### Organize your data

The first step in developing a translation tool is finding texts that can be
used to validate it. For this we need "parallel texts" in the languages we want
to translate between, i.e. texts that are "translation equivalents" and ideally
can be aligned.

#### Get the base text for our source language
For this project we will use the Universal Declaration of Human
Rights as our base text, and our source language will be English. The UDHR base
text for English can be found [here](https://www.unicode.org/udhr/d/udhr_eng.txt).

#### Choose your target language
Choose another UDHR text in a language other than English from the [UDHR unicode page](https://www.unicode.org/udhr/translations.html).

The language you choose should have a Latin-based script and be one for which a
dictionary is readily available (see below). For evaluation purposes, you may
want to choose a language that you have some familiarity with, i.e. [French](https://www.unicode.org/udhr/d/udhr_fra.txt).

Notice how the sentences of the two texts are arranged - this format should
allow you to "align" the sentences so that you can observe the correspondences
between them. This will help with your evaluation later on.

#### Find or develop a bilingual dictionary
Next, find a bilingual dictionary resource that lists words in English and their
corresponding words in the non-English language you chose. Some options can be
found [here](https://www.dicts.info/uddl.php) but you may also want to look for
other sources or develop your own.

### Translate each sentence using the dictionary

Using your bilingual source (wordlist/dictionary), translate each English
sentence in your aligned text to the target language word-by-word. Then
translate each target language sentence into English using the same resource.
Your result should therefore be four times as long as the original UDHR text,
where each sentence/line has four corresponding alignments:
    1. the English sentence
    2. the target language sentence
    3. the English-to-target translation
    4. the target-to-English translation.

Evaluate the translation and consider how you can improve its quality. See if
you can write additional code that will improve the quality of the translation.

### Output

Write your translations to two text files. The first text file should contain
alignments of 1, 2, and 3 (the English sentence, the target language sentence,
and the English-to-target translation), while the second text file should
contain alignments of 1, 2, and 4 (the English sentence, the target language
sentence, and the target-to-English translation).

Your updated repository should contain the files needed to get the text output:
  - the two relevant texts
  - a bilingual dictionary
  - code (with comments) that generates your two translated text files from
  these resources

Your repository should also contain a PDF with a writeup (max 5 pages)
explaining your thought process and briefly outlining your code. You will
additionally submit this PDF as an assignment on TurnItIn.

In your writeup, consider the quality of the translations you were able to
achieve using a dictionary. Are there other methods you can think of that would
generate a better translation? How does this method of translation compare with
other machine translation systems like Google Translate? How well does the UDHR
text lend itself to translation? Are there other kinds/genres of texts you
could try where your machine translator would perform better? (You can use
these questions as a starting point for your discussion)

***Ensure that your name and matric number are clearly indicated in your code and in your PDF submission.***

***Ensure that your final repository submission does not contain any of the 'starter' code or texts.***

## Bonus
The NLTK library has a `comtrans` module that provides machine learning tools
for translation. You can use this module with an aligned corpus to train a
model to translate between a source and target language. To receive additional
credit for this project, use the aligned UDHR texts that you created in the
first part to train a translation model. Then use that model to translate from
the source to the target text. This will require some research on your part to
understand the module and how to format your aligned texts appropriately.

Write this output to another text file containing the aligned English sentences,
target language sentences and the English-to-target translations. In your PDF
writeup, discuss how well it performs in relation to your simpler dictionary-based
translation, and consider reasons why. Your writeup page limit is increased to
6 pages to allow for the bonus discussion.
