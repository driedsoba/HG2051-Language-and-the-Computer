## Name: Liw Jun Le
## Matric Number: U2221922D

from nltk.translate import IBMModel1, AlignedSent
from nltk.tokenize import word_tokenize

# Define the tokenizer function
def tokenize_text(sentence):
    """Tokenize a sentence into words."""
    return word_tokenize(sentence.lower())


# Define the translation function using IBM Model 1
def translate_sentence(english_sentence, model):
    """Translate an English sentence to French using IBM Model 1."""
    words = tokenize_text(english_sentence)
    translation = []
    for word in words:
        translations = model.translation_table.get(word, {})
        if translations:
            best_match = max((w for w in translations if w != ';'), key=translations.get, default=';')
            translation.append(best_match)
        else:
            translation.append(word)
    return ' '.join(translation).capitalize()


# Function to read sentences from a file
def read_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    return [line.strip() for line in sentences if line.strip()]


# Function to remove semicolons from lines starting with "En-Fr:"
def remove_semicolons_from_enfr_lines(text):
    lines = text.split('\n')
    modified_lines = []
    for line in lines:
        if line.startswith('En-Fr:'):
            # Remove semicolons from the line
            line = line.replace(';', '')
        modified_lines.append(line)
    return '\n'.join(modified_lines)


# Define the path to your English and French UDHR files
path_to_english = 'english_udhr.txt'
path_to_french = 'french_udhr.txt'


# Read the English and French sentences
english_sentences = read_sentences(path_to_english)
french_sentences = read_sentences(path_to_french)


# Remove headers and non-content text
english_sentences = english_sentences[english_sentences.index('---') + 1:]
french_sentences = french_sentences[french_sentences.index('---') + 1:]


# Tokenize the sentences
english_tokenized = [tokenize_text(sentence) for sentence in english_sentences]
french_tokenized = [tokenize_text(sentence) for sentence in french_sentences]


# Create aligned sentence pairs for the model
aligned_text = [AlignedSent(en, fr) for en, fr in zip(english_tokenized, french_tokenized)]


# Train the IBM Model 1
ibm_model = IBMModel1(aligned_text, 5)


# Translate the English sentences using the trained model
translated_sentences = [translate_sentence(sentence, ibm_model) for sentence in english_sentences]


# Format the output with the specified prefixes and numbering
output_lines = []
for idx, (en, fr, trans) in enumerate(zip(english_sentences, french_sentences, translated_sentences), start=1):
    output_lines.append(f"{idx} En: \t{en}")
    output_lines.append(f"Fr: \t{fr}")
    output_lines.append(f"En-Fr: \t{trans}\n")


# Prepare the output text with the correct formatting
output_text = "\n".join(output_lines)


# Write the output text to a file
output_path = 'output_en_fr_bonus.txt'
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(output_text)