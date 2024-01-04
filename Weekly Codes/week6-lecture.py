# # Week 06

# Overview
# * File Systems and Paths   
#   import os
#   path = os.path.join('path', 'to', 'file.txt')  # path/to/file.txt
#   filename = os.path.basename(path)
#   directory = os.path.dirname(path)
#   
# * Strings and Bytes 
#   'string'
#   b'bytes'
# 
# * **Buffers**
#   * Opening URLs
#     from urllib import request
#     response = request.urlopen(...)
#     data = response.read()
#   
#   * Opening Files
#     with open('output.txt', mode='w') as outfile:
#         print(data, file=outfile)
# 
# * Strings and Bytes Part II
#   $ python
#   >>> 'café'.encode('utf-8')
#   b'caf\xc3\xa9'
#   >>> b'caf\xc3\xa9'.decode('utf-8')
#   'café'
# 
# * [Exercise](#Exercise)
#   * Get a text file from http://www.gutenberg.org/ and read it in
#   * Remove the non-content text
#   * Generate some metadata
#   * Save it to a file
#   * Do some NLTK operations on it

# ## File Systems and Paths
# Before we get to buffers, let's look briefly at paths. When 
# you access something on the file system (a file on your computer),
# you use paths. In Windows these look like `C:\Documents\My File.txt` 
# while on macOS (and Linux, roughly) they look like 
# `/Users/username/Documents/My File.txt`. Notice that Windows 
# paths have a "drive letter" (`C:`) where macOS and Linux paths 
# do not. Also the slashes go different directions.

# Python provides the `os.path` module to help with these differences. 
# For example:
import os
path = os.path.join('~', 'Documents', 'My File.txt')  # ~ is special: it's the user's home directory
print(path)
path = os.path.expanduser(path)  # Use expanduser() to convert ~ to the actual path
print(path)
print(os.path.exists(path))
print(os.path.basename(path))  # just the file
print(os.path.dirname(path))  # just the directory

# ## Strings and Bytes
# Very briefly let's look at the difference between strings 
# and byte strings. In Python, a string (`str`) is a sequence 
# of unicode codepoints. That is, it is an abstraction that 
# provides a pure representation of unicode characters. In 
# contrast, byte strings (`bytes`) are the concrete *encoding* 
# of unicode into some sequence of `1`s and `0`s that a computer 
# can store or transmit. There are many ways (encodings) that 
# unicode can be encoded into bytes, but the most popular one 
# these days is UTF-8. Also, unlike strings, byte strings can 
# contain non-textual data (images, audio, etc.), but we will 
# not cover this usage in this course.

# In Python, strings are represented just as characters in quotes:
#
'single quotes'
"double quotes"
'''three-in-a-row single quotes'''
"""three-in-a-row double quotes"""
#

# Bytes are about the same, but prefixed with a `b`:
# 
b'single quotes'
b"double quotes"
b'''three-in-a-row single quotes'''
b"""three-in-a-row double quotes"""
#

# * Question: if bytes are just `1`s and `0`s, why do we see 
# characters in Python code?

# The answer is that Python, like most programming languages, 
# allows you to write code in a human-readable form using ASCII 
# characters. But the bytes that are actually stored are not 
# ASCII, but rather are encoded in UTF-8. So the byte string 
# `b'café'` is actually stored as `b'caf\xc3\xa9'` (see below).
# Later (below) we will talk about converting between strings and bytes.

# ## Buffers
# Buffers are like queues (here, people waiting for the iPhone 11 
# in Singapore):
# <img src="https://pbs.twimg.com/media/EE3NDcrU8AA70H1.jpg" 
# alt="People queueing for the iPhone 11 in Singapore" width="60%"/>

# Stuff goes in one end and comes out the other, but you don't know 
# how long (how many people, or bytes) it will be until you get to 
# the end. Strings, lists, tuples, dicts, and sets in Python are 
# fixed-length **collections**, so you can do `len(x)` to get the 
# number of items in `x` and iterate over their contents. Strings, 
# tuples, and lists are also **sequences**, so you can access an 
# item at any position ("random access"). Buffers are only iterable: 
# you cannot do `len(some_buffer)` or get random access (`some_buffer[5]`).

# What are buffers used for?
# * Opening files on your computer
# * Sockets (e.g., web connections)
# * standard streams, string buffers, etc. (not covered in class)

# Buffers also work on bytes, not unicode characters, as (a) they 
# may transmit non-textual information, and (b) unicode characters 
# (e.g., encoded into UTF-8) are not fixed-size. Python, however, 
# often deals with the encoding and decoding for you, but you'll 
# need to know when it doesn't.

# * Questions:
#   - How can you tell if something is a string or bytes?
#   if isinstance(variable, str):
#    print("It's a string")
#   elif isinstance(variable, bytes):
#    print("It's bytes")
#   - How can you find out the encoding? 
# encodings_to_try = ['utf-8', 'latin-1', 'utf-16']
# for encoding in encodings_to_try:
#    try:
#        text = binary_data.decode(encoding)
#        print(f"Decoded using {encoding}: {text}")
#        break
#    except UnicodeDecodeError:
#        continue

# First let's set up a temporary directory to work with:
import os
import tempfile
tempdir = tempfile.TemporaryDirectory()
dirname = tempdir.name  # the path to the temporary directory

# ### Opening URLs
# Now lets retrieve some data from the web (a socket buffer) and 
# write it to a file (a file buffer):
from urllib import request
url = 'http://www.gutenberg.org/files/35/35-0.txt'  # H.G. Wells "The Time Machine"
response = request.urlopen(url)  # response is a HTTPResponse buffer object
data = response.read()           # get the data (don't wait too long with web connections)
print(data[:100])  # inspect the first 100... characters? bytes?

# ### Opening Files
# Now let's write either `data` to a file using the `open()` 
# function, which returns a file buffer. The best way to use this 
# is in a `with` statement, as shown below. Pay attention to the
# 'mode' flag, as this conditions how the object gets read or
# written:
# 
path = os.path.join(dirname, 'the-time-machine.txt')
with open(path, mode='wb') as outfile:  # wb = write-bytes, outfile is the buffer object
    outfile.write(data)
print(dirname)
print(outfile)

# We can read back the file as bytes:
with open(path, mode='rb') as infile:  # rb = read-bytes, infile is the buffer object
    tmpdata = infile.read()
print(tmpdata[:100])

# 
# We can also read it back as a string (**note**: on Windows you 
# may need to specify the encoding as `utf-8-sig`; on macOS and 
# Linux you can probably just use the default value of `utf-8`):
with open(path, mode='r', encoding='utf-8-sig') as infile:  # r = read-text
    tmpdata = infile.read()
print(tmpdata[:100])

# 
# And we can write a file with a string instead of bytes:
another_path = path + '2'
with open(another_path, mode='w') as outfile:  # w = write-text
    outfile.write(tmpdata)

# 
# Now let's check that these two files are the same:
with open(path, mode='r', encoding='utf-8-sig') as infile:
    txt1 = infile.read()

with open(another_path, mode='r') as infile:
    txt2 = infile.read()
    
print(txt1 == txt2)

# What about the encoding? By default it is 'utf-8', but you 
# can provide a different one with the `encoding` parameter, 
# as shown here (but we won't execute it):
# 
# with open(path, mode='r', encoding='ascii') as infile:
#     infile.read()  # might crash if file is not ASCII-compatible!
#

# You can also set the encoding when writing a file, but only 
# when writing text, not bytes.
# 
# Finally, another useful way to open files is to directly 
# iterate over them, which splits the file into lines and 
# iterates over them:
# 
linecount = 0
wordcount = 0
for line in open(path, encoding='utf-8-sig'):  # by default, mode='r'
    linecount += 1
    wordcount += len(line.split())

print('The file has {} lines and {} words'.format(linecount, wordcount))


# ## Strings and Bytes Part II
# Let's return to the topic of strings and bytes. Above we took 
# the `bytes` object returned by the `HTTPResponse` buffer and 
# wrote it to a file then read it in as a string. But we can do 
# the encoding and decoding directly. Note:
# 
# * `bytestring.decode(encoding)` -- decode *bytestring* to unicode using *encoding*
# * `string.encode(encoding)`  -- encode *string* to bytes using *encoding*
data[:100]
text = data.decode('utf-8')
text[:100]
text.encode('utf-8')[:100]

# You can also choose a different encoding for conversion, but 
# be aware that non-unicode encodings (UTF-8, UTF-16, etc.) 
# may not have a way to represent some codepoints, and you'll 
# get an error (uncomment to see the error):
# text.encode('ascii')

# What is that `\ufeff`? That's a **unicode escape**, a way to 
# represent a unicode codepoint. We can evaluate it:
print('\ufeff')
# `\ufeff` is a special spacing character which is not representable 
# in the `ascii` encoding. It's also a Byte Order Mark (BOM).


# ## Exercise
#   * Get a text file from http://www.gutenberg.org/ and read it in
#   * Remove the non-content text
#   * Generate some metadata
#   * Save it to a file
#   * Do some NLTK operations on it
# 
url = 'http://www.gutenberg.org/files/22139/22139-0.txt'
bytestring = request.urlopen(url).read()
bytestring[:50]
text = bytestring.decode('utf-8')
print(repr(text[:50]))
# 
# If the string starts with \ufeff, then you're seeing the BOM 
# signature. Try re-decoding using 'utf-8-sig' instead.
# 
text = bytestring.decode('utf-8-sig')
print(repr(text[:50]))
len(text.splitlines())
len(text.split())
text.index('KARLMENN')  # start is around this string
start = 690  # manually determined 690 as the start
end = text.index('End of Project Gutenberg\'s')
story = text[start:end]
print(story[:50])
print(len(story.splitlines()))

# 
# try to make an NLTK Text object out of it
import nltk
t = nltk.Text(story.split())
t.concordance('verður')
print(nltk.FreqDist(story.split()).most_common(20))

# ## Text Distance Metrics
# Just as you can calculate the distance between two points in 
# a euclidean space, you can compute the distance between two 
# strings. There are multiple ways to do so. Below are some 
# provided by the NLTK. Note that some work on strings and 
# some work on sets:
# 
from nltk.metrics import distance
print(distance.binary_distance('abc', 'bcd'))
print(distance.jaccard_distance(set('abc'), set('bcd')))
print(distance.masi_distance(set('abc'), set('bcd')))
print(distance.edit_distance('abc', 'bcd'))

# The `edit_distance()` metric is also called the 
# Levenshtein Distance (https://en.wikipedia.org/wiki/Levenshtein_distance). 
# Peter Norvig (Director of Research at Google) once created a 
# spell checker in a few dozen lines of Python using Levenshtein 
# Distance and wrote a nice article about it: http://norvig.com/spell-correct.html.

# ## Cleanup
tempdir.cleanup()  # run this when you're done to delete the temporary directory
print(os.path.exists(dirname))
