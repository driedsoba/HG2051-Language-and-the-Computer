## Name: Liw Jun Le
## Matric Number: U2221922D

import json # Import JSON module for saving and loading the dictionary
import nltk # Import NLTK for lemmatization and POS tagging
import spacy # Import spaCy for French lemmatization
from nltk.corpus import wordnet # Import WordNet lexical database
from nltk.stem import WordNetLemmatizer # Import WordNetLemmatizer to lemmatize English words
from nltk.tokenize import word_tokenize # Import word_tokenize to tokenize sentences

# Set up the WordNet lemmatizer and spaCy French model
wn_lemmatizer = WordNetLemmatizer() # WordNet lemmatizer
nlp_fr = spacy.load('fr_core_news_sm')  # spaCy French model


def lemmatize_sentence_en(sentence):
    """Lemmatize an English sentence and return lemmas with POS tags."""
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    return [
        (wn_lemmatizer.lemmatize(word, tag_dict.get(pos[0], wordnet.NOUN)), pos)    # Lemmatize based on POS tag
        for word, pos in pos_tagged     # Iterate through the POS tagged sentence
    ]


def lemmatize_sentence_fr(sentence):
    """Lemmatize a French sentence and return lemmas with POS tags."""    
    doc = nlp_fr(sentence)  # Parse the sentence with spaCy
    return [(token.lemma_, token.pos_) for token in doc]    # Return lemmas and POS tags


def translate_word(word, pos, dictionary, lang):
    """Translate a word based on the provided dictionary and language direction."""
    key = f'{word.lower()}_{pos}'   # Create a key for the dictionary lookup
    if key in dictionary:           # Check if the key is in the dictionary
        return dictionary[key].split('_')[0]    # Return the translation if found
    
    if word.lower() in dictionary:  # Check if the word is in the dictionary
        return dictionary[word.lower()].split('_')[0]   # Return the translation if found
    
    return word  # Return the original word if no translation is found


def translate_text(text, dictionary, reverse_dict, lang):
    """Translate a text based on the provided dictionary and language direction."""
    lemmatized_pos_tagged = (
        lemmatize_sentence_en(text) if lang == 'en' else lemmatize_sentence_fr(text) # Lemmatize the text
    )
    translated = [
        translate_word(lemma, pos, dictionary if lang == 'en' else reverse_dict, lang) # Translate each word
        for lemma, pos in lemmatized_pos_tagged                                        # Iterate through the lemmas
    ]
    return ' '.join(translated).capitalize() 


def build_dictionary(en_file_path, fr_file_path, dictionary_path):
    """Build a dictionary from aligned English and French UDHR texts."""
    # Open the English and French UDHR texts, skip front matter
    with open(en_file_path, 'r', encoding='utf-8') as en_file, \
         open(fr_file_path, 'r', encoding='utf-8') as fr_file:

        en_lines = en_file.readlines()[6:]
        fr_lines = fr_file.readlines()[6:]

        dictionary = {}
        for en_line, fr_line in zip(en_lines, fr_lines):
            add_to_dictionary(en_line.strip(), fr_line.strip(), dictionary)

        save_dictionary(dictionary, dictionary_path)
        return dictionary


def reverse_dictionary(dictionary):
    """Generate a reversed dictionary for the opposite language direction."""
    return {value: key.split('_')[0] for key, value in dictionary.items()} # Reverse the key-value pairs


def add_to_dictionary(en_sentence, fr_sentence, dictionary):
    """Add translation pairs to the dictionary based on aligned sentences."""
    en_lemmas = lemmatize_sentence_en(en_sentence)  # Lemmatize the English sentence
    fr_lemmas = lemmatize_sentence_fr(fr_sentence)  # Lemmatize the French sentence
    for (en_lemma, en_pos), (fr_lemma, fr_pos) in zip(en_lemmas, fr_lemmas):    # Iterate through the lemmas
        dictionary[f'{en_lemma.lower()}_{en_pos}'] = f'{fr_lemma.lower()}_{fr_pos}' # Add translation pair to dictionary


def save_dictionary(dictionary, file_path):
    """Save the dictionary to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:    # Open the file for writing
        json.dump(dictionary, file, ensure_ascii=False, indent=4)   # Write the JSON data


def load_dictionary(file_path):
    """Load the dictionary from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:    # Open the file for reading
        return json.load(file)  # Return the JSON data


def main():
    """Main function to load/create dictionary and generate translations."""
    dictionary_path = 'dictionary.json'   # Path to the dictionary file
    try:
        dictionary = load_dictionary(dictionary_path)  # Load the dictionary if it exists
    except FileNotFoundError:
        dictionary = build_dictionary('english_udhr.txt', 'french_udhr.txt', dictionary_path)  # Build the dictionary

    reverse_dict = reverse_dictionary(dictionary)  # Generate the reverse dictionary for French to English translation

    # Open the English and French UDHR texts
    with open('english_udhr.txt', 'r', encoding='utf-8') as en_file, \
         open('french_udhr.txt', 'r', encoding='utf-8') as fr_file, \
         open('output_en_fr.txt', 'w', encoding='utf-8') as output_en_fr, \
         open('output_fr_en.txt', 'w', encoding='utf-8') as output_fr_en:

        en_lines = [line.strip() for line in en_file.readlines() if line.strip()]
        fr_lines = [line.strip() for line in fr_file.readlines() if line.strip()]

        # Find the index of the content separator
        try:
            start_index = en_lines.index('---') + 1
        except ValueError:
            start_index = 0  # If separator not found, start from the beginning

        # Translate and write the results starting from the content after the separator
        for i, (en_line, fr_line) in enumerate(zip(en_lines[start_index:], fr_lines[start_index:]), start=1):
            en_to_fr = translate_text(en_line, dictionary, reverse_dict, 'en')  # Translate English to French
            fr_to_en = translate_text(fr_line, reverse_dict, dictionary, 'fr')  # Translate French to English

            output_en_fr.write(f"{i} En:\t{en_line}\nFr:\t{fr_line}\nEn-Fr:\t{en_to_fr}\n\n")  # Write to output En-Fr file
            output_fr_en.write(f"{i} Fr:\t{fr_line}\nEn:\t{en_line}\nFr-En:\t{fr_to_en}\n\n")  # Write to output Fr-En file

if __name__ == "__main__":
    main()  # Run the main function
