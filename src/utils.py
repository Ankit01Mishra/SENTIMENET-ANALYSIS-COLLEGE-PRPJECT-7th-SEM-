"""
Author: Ankit Kumar
Date: 6-sep-2019
email: akmishra98cse@gmail.com
"""

# Imports
# configuring nltk
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

import codecs
import unidecode
import re
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from src.contraction_mapping import contraction_mapping

nlp = spacy.load('en')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def basic_clean(text):
    """
    This function lemmatizes the text.
    :param text: Text (sentence)
    :return: clean text
    """
    text = re.sub(r'[^\w\s]', '', text, re.UNICODE)
    text = text.lower()
    text = [lemmatizer.lemmatize(token) for token in text.split(" ")]
    text = [lemmatizer.lemmatize(token, "v") for token in text]
    text = [word for word in text if not word in stop_words]
    text = " ".join(text)
    return text


def spacy_cleaner(text):
    """
    :param text: Sentence
    :return: clean - text
    """

    try:
        decoded = unidecode.unidecode(codecs.decode(text, 'unicode_escape'))
    except:
        decoded = unidecode.unidecode(text)
    apostrophe_handled = re.sub("’", "'", decoded)
    expanded = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in apostrophe_handled.split(" ")])
    parsed = nlp(expanded)
    final_tokens = []
    for t in parsed:
        if t.is_punct or t.is_space or t.like_num or t.like_url or str(t).startswith('@'):
            pass
        else:
            if t.lemma_ == '-PRON-':
                final_tokens.append(str(t))
            else:
                sc_removed = re.sub("[^a-zA-Z]", '', str(t.lemma_))
                if len(sc_removed) > 1:
                    final_tokens.append(sc_removed)
    joined = ' '.join(final_tokens)
    spell_corrected = re.sub(r'(.)\1+', r'\1\1', joined)
    return spell_corrected


