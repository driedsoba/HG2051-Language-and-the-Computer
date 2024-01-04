# # Week 6
# This week is about getting data into Python from external 
# sources, such as files on your computer or online. When working 
# with these kinds of sources, we need to understand **character 
# encodings** and **streams**. This week we will also cover **string 
# formatting**, as it is useful when writing to files or to the 
# terminal. Additionally, various Python libraries have been 
# developed to handle different filetypes - we will use the `pandas` 
# library to import/modify/export spreadsheet files.

# import nltk  # make sure NLTK is installed and loaded

# ## Unicode
# Every character displayed by your computer is assigned a number. 
# When computers were initially developed, each character set (e.g., 
# for a language) chose different numbers for the characters, but 
# this made it difficult to have documents with more than one 
# character set. Unicode (https://unicode.org/) is the modern 
# standard for assigning these numbers, and it is one giant table 
# comprising all the known characters, including some non-language 
# characters (🥳🦥🌤...). In Python, strings are "pure" sequences 
# of codepoints. You can find the codepoint (as an integer) of a 
# character with Python's `ord()` function, and the character for 
# a codepoint with the `chr()` function:
print(ord('Z'))
print(chr(129445))

# In practice these two functions are used rarely, however.

# ## Encodings
# Whenever a unicode string needs to be stored or transmitted 
# outside of Python it must be encoded into a sequence of bytes.
'あ'.encode('utf-8')
# Similarly, bytes can be decoded to strings:
b'\xe3\x81\x82'.decode('utf-8')
# Notice that the `bytes` objects (the strings prefixed with `b`) 
# use escape sequences to represent the bytes, such as `\xe3` 
# which represents the bits `1110 0011` (note: you do not need 
# to know this conversion). Python also accepts escape sequences 
# in regular strings, but numbers do not represent UTF-8 or some 
# other encoding, but the numeric value of the codepoint (you do 
# not need to learn these escapes, just recognize that `\x`, `\u` 
# and `\U` followed by 2, 4, or 8 hexadecimal digits (0123456789ABCDEF) 
# is a unicode escape).
print('\u3042')

# Aside: If you want to find out the decimal value of the hexadecimal 
# number, use the `int()` function with a base of 16:
print(int('3042', 16))
# And you can get back the hexadecimal version with `hex()`:
print(hex(12354))

# If you try to encode something not representable in the target 
# encoding, you'll get an error. In this case, the letter 'é' is 
# not part of the `ascii` encoding (uncomment to see the error):
# print('café'.encode('ascii'))
# You can tell Python what to do in case of errors, such as ignoring them (note that the letter doesn't appear in the output):
print('café'.encode('ascii', errors='ignore'))

# ## Streams
# When you have a string in Python, you have the entire contents 
# and you can query its length or access any character at once. 
# When you're working with *streams*, however, you only get a small 
# slice, or window, at a time. This is useful when the data is too 
# large to fit into memory (like a dump of all of Wikipedia), or 
# something that is slow to download.

# Here we will download the text of a book from Project Gutenberg 
# (not using the NLTK):
import urllib.request

# # urlopen() returns a stream, but then we call .read(), which 
# fetches the whole thing.
# # The result is a bytes object, not str.
bytestring = urllib.request.urlopen('http://gutenberg.org/files/13083/13083-0.txt').read()

print(type(bytestring))
# Depending on the language, the data may not be very readable:
print(bytestring[1004:1046])
# So we need to decode it:
string = bytestring.decode('utf-8')
print(type(string))
# Now we can read the string (if we could read Czech). Note that 
# the indices of the bytestring don't always line up with those of 
# the string.
print(string[974:1013])
# We can also read and write files on disk using `open()`. Let's 
# write the downloaded bytes directly to disk using `open()`'s `wb` 
# ("write bytes") mode:
with open('myfile.txt', 'wb') as f:
    f.write(bytestring)
# Now confirm that we have written the file. You may need to change 
# the encoding from `utf-8` to `utf-8-sig` on Windows.
with open('myfile.txt', encoding='utf-8') as f:
    string = f.read()
print(string[:100])

# Instead of writing bytes directly, if you have the decoded string 
# you can write in "text" mode (`wt`, or just `w`). In this case, 
# it's best to specify your desired encoding. Also note that instead 
# of `f.write(bytestring)`, you can use `print(string, file=f)`.
with open('myfile2.txt', 'wt', encoding='utf-8') as f:
    print(string, file=f)

# ## String Formatting
# When printing to the terminal or writing to disk, sometimes it 
# helps to format the strings so they are more legible or so they 
# follow a particular file format. The `str.format()` method or 
# "f-strings" are two common ways to do so (see this week's reading 
# for explanation of these).

# Write some code that takes a string and prints a table of each 
# letter found in the string with its frequency. The frequency should 
# be right aligned so number columns (ones, tens, etc.) line up. 
# Don't use NLTK's `nltk.FreqDist.tabulate()` method, but you may use 
# `nltk.FreqDist` to get the frequency information. You may choose to 
# filter out non-letter characters.
# recall we can get the frequency distribution of a sequence (of words, 
# or characters, etc.) with nltk.FreqDist
import nltk
with open('myfile.txt', encoding = 'utf-8') as f:
    # `f.read()` returns the full string of the file
    # `if c.isalpha()` only keeps alphabetic characters (optional)
    fd = nltk.FreqDist(c for c in f.read() if c.isalpha())
print(fd)
# For our table, we can use a fixed width between the character 
# and the count, but here I first calculate the largest frequency 
# then find its width when it is a string. This is the widest number 
# that we will display. (This step is optional).
maximum = max(fd.values())
width = len(str(maximum)) 

# Next we go over each letter in most-common-first order, then 
# print the letter, a tab character (`\t`), then the count right 
# aligned in a span using the width we just calculated.
for c, count in fd.most_common():
    # here I use f-string formatting. The same could be done with:
    # print('{c}\t{count:>{width}}'.format(c=c, count=count, width=width))
    print(f'{c}\t{count:>{width}}')

# ## Working with non-text files
# The [Pandas](https://pandas.pydata.org/) library makes it easy 
# to work with both CSV/TSV and XLSX file types. We will convert 
# the frequency distribution we made from our file into a `DataFrame`.

# (if you get a "module not found" error, you need to `pip install` 
# the module in your virtual environment via your terminal)
import pandas as pd
# create lists from the keys and values in the dict (how would 
# you rewrite this as a list comprehension?)
chars, nums = [], []
for k, v in fd.items():
    chars.append(k)
    nums.append(v)

chars = list(fd.keys())
nums = list(fd.values())

# we instantiate an empty dataframe here
df = pd.DataFrame()
# we create two new column headers, populating the columns with 
# the two lists
df['characters'], df['numbers'] = chars, nums
# then we view the first 5 rows
print(df.head())

# When you have a dataframe, Pandas automatically populates 
# the "index" value on the left hand side, which you can then 
# use to refer to the row. Dataframes resemble lists and dicts, 
# in that you can get their length (number of rows), you can 
# perform operations on them, you can get slices from them, and 
# you can convert them to/from lists/dicts. Think of a dataframe 
# as a collection of lists where either the index or the header 
# can be the key.
print(len(df))
# we create a new column 'divided by 2' and set the values equal 
# to every corresponding value in the 'numbers' column divided by 2
df['divided by 2'] = df['numbers']/2 
print(df.head())

charlist = df['characters'].tolist() # make a list from the 'characters' column
if charlist == chars: # check if this the same as the list we created earlier?
    print("yes")
# we can create a dataframe directly from our frequency dict
df = pd.DataFrame.from_dict(fd.items()) # you must use `.items()` here
print(df.head()) # notice that the column headers are integers `0` and `1` by default
# we can create a dictionary from our dataframe, using the first 
# column as the index (key) and the second as the value

newfd = df.set_index(0)[1].to_dict()
print(newfd)

# We can write this data to a file in CSV or XLSX format using Pandas. 
# To work with XLSX you may need to install the `openpyxl` library via pip.
print(list(df.columns)) # see what the column names are
df.columns = ['characters', 'numbers'] # set the column names manually
print(df.head())

df.to_csv("myfile.csv", sep="\t") # write to csv using tab as delimiter
df = pd.read_csv("myfile.csv", delimiter="\t") # read from csv using tab as delimiter
print(df.head()) # notice that it imports the index line as the first column

# we can delete the first column by simply excluding it in our list of columns
df = df[['characters', 'numbers']]
# when we export it (this time as XLSX) we can use the 'index=False' flag to not write the index
df.to_excel('myfile.xlsx', index=False) # with excel export/import we don't need a delimiter
# then we can import it again
xdf = pd.read_excel('myfile.xlsx')
print(xdf.head())