# # Week 08

# Overview

# * **Regular Expressions**

#   * [What?](#...What?)
#   * [Why?](#Why?)
#   * [How?](#How?)

# * [How to Craft Regular Expressions](#How-to-Craft-Regular-Expressions)

#   * [Escaping](#Escaping)
#   * [Sequences, Choices, and Greedy Matching](#Sequences,-Choices,-and-Greedy-Matching)
#   * [Repetition](#Repetition)
#   * [Anchors](#Anchors)
#   * [Character Classes](#Character-Classes)
#   * [Groups](#Groups)

# * [How to Replace Text with Regular Expressions](#How-to-Replace-Text-with-Regular-Expressions)

# * [Exercises](#Exercises)

# # Regular Expressions

# Regular expressions ("regex") are patterns defined in a mini-language for describing small grammars that match strings.

# ## ...What?

# Consider a formal grammar for matching laughter in multiple languages:

# Start  := "5" Tha
#         | "ha" Eng
#         | "je" Spa
#         | "w" Jp1
#         | "笑" Jp2
#         | "哈" Ch1
#         | "呵" Ch2
#         | "ke" Ko1
#         | "k" Ko2
# Tha    := "5" Tha | "5"
# Eng    := "ha" Eng | "ha"
# Spa    := "je" Spa | "je"
# Jp1    := "w" Jp1 | "w"
# Jp2    := "笑" Jp2 | "笑"
# Ch1    := "哈" Ch1 | "哈"
# Ch2    := "呵" Ch2 | "呵"
# Ko1    := "ke" Ko1 | "ke"
# Ko2    := "k" Ko2 | "k"

# **Q:** Is this grammar regular? If so, is it right-regular or left-regular?

# **NB:** Regular expression engines today, such as the one for Python, 
# employ features beyond what's allowed by "regular grammars".

# The grammar above matches when a laughter sound occurs two or more times.
# We could write that in Python code like this:

def match_laughter(s):
    i = 0
    if s.startswith('55'):
        i = match_thai(s, 2)
    elif s.startswith('haha'):
        i = match_english(s, 4)
    elif s.startswith('jeje'):
        i = match_spanish(s, 4):
    elif ...
    # etc...
    if i > 0:
        return s[:i]
    else:
        return None

def match_thai(s, i):
    if s[i] == '5':
        i = match_thai(s, i+1)
    return i

def match_english(s, i):
    ...
# etc...

# ... but that is a lot of code. Instead we could use a regular expression
#  to write it more concisely:

# 55+|ha(ha)+|je(je)+|ww+|笑笑+|哈哈+|呵呵+|ke(ke)+|kk+

# This regular expression is equivalent to the grammar above and matches
# the same strings.

# ## Why?

# Regular expressions are a bit hard to read, but they allow you to quickly 
# write out a query for complex patterns. See this XKCD comic for motivation:

# <a href="https://xkcd.com/208/"><img src="https://imgs.xkcd.com/comics/regular_expressions.png" width="60%" title="Wait, forgot to escape a space.  Wheeeeee[taptaptap]eeeeee."></a>

# But regular expressions are a skill to learn and take time to master, 
# leading to (slightly demotivating) quotes like the following:

# On 12 August, 1997, Jamie Zawinski said:
# > Some people, when confronted with a problem, think “I know,
# > I'll use regular expressions.”  Now they have two problems.

# (paraphrasing a previous quote by D. Tilbrook; [source](http://regex.info/blog/2006-09-15/247))

# This joke was adapted into the following XKCD comic:

# <a href="https://xkcd.com/1171/"><img src="https://imgs.xkcd.com/comics/perl_problems.png" title="To generate #1 albums, 'jay --help' recommends the -z flag."></a>

# ## How?

# The `re` module is part of Python's standard library:
import re
# It has many useful functions. The following are the more important ones:

# * [re.search(pattern, string)](https://docs.python.org/3/library/re.html#re.search)
#   matches anywhere in the string
#   - [re.match()](https://docs.python.org/3/library/re.html#re.match) and
#     [re.fullmatch()](https://docs.python.org/3/library/re.html#re.fullmatch) are similar
# * [re.findall(pattern, string)](https://docs.python.org/3/library/re.html#re.findall)
#   list of all matches in the string
# * [re.sub(pattern, repl, string)](https://docs.python.org/3/library/re.html#re.sub)
#   "substitute": replace matches in the string with a replacement
# * [re.split(pattern, string)](https://docs.python.org/3/library/re.html#re.split)
#   split on matches

# For example, if we adapt our previous example to detect excessive laughter, but not just mild amusement, multilingually:
re.findall('555+|(?:ha){3,}|(?:je){3,}|[w笑]{3,}|[哈呵]{3,}|ke{3,}|k{3,}',
           '555555555555 haha hahaha jeje wwww 笑笑 哈哈哈 kekeke 5hajew笑哈ke')

# Next we will look at how to create patterns like the one above.

# # How to Craft Regular Expressions

# Regular expression patterns are defined as a string. Some characters 
# have special meaning and others are literal. Some special characters 
# allow for flexible matches and others are like control flow structures.

# ## Escaping

# First, character escapes are very common in regular expressions. Recall 
# that you can escape characters like newlines (`\n`) and tabs (`\t`) with 
# the backslash character (`\`). In regular expressions, characters with 
# special meaning can be escaped to match the literal character, and some 
# literal characters can be escaped to give them a special meaning. For 
# example, the pipe character `|` has special meaning in regexes (described 
# below), but `\|` matches the character itself. The `w` character is literal, 
# but `\w` matches "word" characters (similar to Python's `str.isalnum()`). 
# Also, because the backslash is used both as escapes for regular expressions 
# **and** for the Python strings that contain the patterns, you need to escape 
# the backslashes themselves. For example, the following pattern (as a Python 
# string) matches a word character followed by a pipe character:

'\\w\\|'

# Fortunately, Python has *raw strings* prefixed with `r` that reduce the 
# need for escaping. The same pattern as above can be written more naturally 
# as follows:

r'\w\|'

# If you're having trouble with patterns matching, double-check that you're 
# using a raw string.

# ## Sequences, Choices, and Greedy Matching

# Sequential sub-patterns are matched sequentially, so `abc` does not 
# match "cba". The pipe character (`|`) has the meaning "or", so `abc|cba` 
# matches both "abc" and "cba", but not "acb", "bac", "bca", or "cab". 
# Choices are **greedy**, meaning that they choose the first match. For 
# example, the pattern `abc|cba`, when applied to "abcba", would match 
# "abc" but not "cba", because it first matches "abc" and *consumes* these 
# characters, so the "c" is not available for matching "cba". This is 
# illustrated below:

# Pattern: abc|cba

# Input:     abcba
# Match:     abc
# Remainder:    ba  <-- does not match

# Input:     cbabc
# Match:     cba
# Remainder:    bc  <-- does not match

# re.findall()

# ## Repetition

# Characters and subpatterns can be repeated via several mechanisms. The 
# most basic are `*` and `+` ([Kleene star/plus](https://en.wikipedia.org/wiki/Kleene_star)), 
# as well as `?`:

# * `a*` : match "a" zero or more times
# * `a+` : match "a" one or more times
# * `a?` : match "a" zero or one time (optionality)

# Some more control is given by the use of braces (`{}`) with specific numbers:

# * `a{3}` : match "a" 3 times exactly
# * `a{3,5}` : match "a" between 3 and 5 times
# * `a{3,}` : match "a" 3 or more times
# * `a{,5}` : match "a" 5 or fewer times

# ## Anchors

# With `re.search()` and `re.findall()`, the pattern matches anywhere in 
# the input string. Anchors are used to ensure that the pattern only matches 
# at the start or end of a string:

# * `^` the start of the string
# * `$` the end of the string

# Note that these are special characters. Also, they are zero-width matches, 
# meaning they do not consume any input (e.g., they do not consume the first 
# or last characters of the string).
re.search(r'', '')  # '' in str (no anchors)
re.search(r'', '')  # str.startswith()
re.search(r'', '')  # str.endswith()

# ## Character Classes

# Character classes are sub-patterns contained in square brackets (`[...]`). 
# A character class will match any **one** character it describes. Note 
# that there are some different rules within a character class:

# * `[abc]` : match "a", "b", or "c"
# * `[^abc]` : match any character that is *not* "a", "b", or "c"
# * `[a-z]` : match any character from "a" to "z" (e.g., "b", "c", "d", etc., but not "A", "B", etc.)

# Some predefined character classes are available by escaping literal characters:

# * `\w` : match any word character (letters, digits, some punctuation)
# * `\d` : match any digit character
# * `\s` : match any space character
# * `\b` : match a word boundary (zero-width match)

# There are also the inverses of the above by escaping the upper-case letters:

# * `\W` : match any non-word character
# * `\D` : match any non-digit character
# * `\S` : match any non-space character
# * `\B` : match a non-word-boundary (zero-width match)

# ## Groups

# Sometimes subpatterns need to be repeated or made optional. Patterns 
# contained in parentheses are called *groups*. There are two main kinds 
# of groups:

# * `(...)` : capturing group
# * `(?:...)` : non-capturing group

# The difference is made clear when you start looking at the Match objects 
# returned by `re.search()` or the strings returned by `re.findall()`:
re.search(r'c(ab)+d', 'cabababd').groups()
re.search(r'c(?:ab)+d', 'cabababd').groups()
# The special group index 0 is the entire match, not just the captured groups:
re.search(r'c(ab)+d', 'cabababd').group(0)
re.search(r'c(?:ab)+d', 'cabababd').group(0)

# # How to Replace Text with Regular Expressions

# The `re.sub()` function matches a string and replaces any matches it 
# finds with a replacement pattern. These replacement patterns can reuse 
# parts of the matched string using `\1`, `\2`, etc. for the indices of 
# capturing groups.
re.sub(r'!+', r'!', 'HI!!!!!!!!!!!!!!!!!')
re.sub(r'[Mm]e (and|or) (\w+)', r'\2 \1 I', 'Me or Kim will go.')

# ## Exercises

# Now let's practice:

# * What kinds of strings do the following patterns match:

#   - `[a-zA-Z]+` # letters only
#   - `[A-Z][a-z]*` # capitalized words
#   - `p[aeiou]{,2}t` # words with 0-2 vowels
#   - `\d+(\.\d+)?` # numbers with optional decimal part
#   - `([^aeiou][aeiou][^aeiou])*` # words with alternating vowels and consonants
#   - `\w+|[^\w\s]+` # words or punctuation

# * Following the T9 "textonyms" from the NLTK book, find out what words 
# can be formed using part of your phone number, zip code, etc.

# * Go to http://www.gutenberg.org/catalog/ and get the URL for the plain 
# text version of some book (any language you know). Download and decode 
# it, then look for patterns. Some examples:
#   - English: (x) and (y); (x)ed; (x)ing; the (x)est (y)
#   - Chinese: (x)子; 太(x)了

from urllib import request
text = request.urlopen(...).decode('utf-8')  # or utf-8-sig
