import string
import nltk
import spacy
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer

# Performing NER
def ner(query):
    nlp = spacy.load("en_core_web_sm") # `spacy download en_core_web_sm` in terminal
    doc = nlp(query)

    # Extracting entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return entities

# Correcting spelling and removing spaces
def basic_preprocessing(query):

    # Removing punctuation (except for apostrophes)
    query = ''.join(c for c in query if c not in string.punctuation or c == "'")

    # Removing leading/trailing whitespace
    query = query.strip()

    # Word tokenization
    tokens = nltk.word_tokenize(query)

    # Checking spelling
    spell = SpellChecker()
    corr_tkn = []
    for token in tokens:
        corr_tkn.append(spell.correction(token))
    pre1_qry = ' '.join(corr_tkn)

    entities = ner(query)

    for part in entities:
        pre2_qry = ' '.join(part)
    
    return pre1_qry + ' ' + pre2_qry

# Lemmatization
def lemmatization(query):

    fin_qry = basic_preprocessing(query)

    tokens = nltk.word_tokenize(fin_qry)

    lemm = WordNetLemmatizer()
    lemm_tkn = [lemm.lemmatize(token) for token in tokens]

    preprocessed_query = ' '.join(lemm_tkn)

    return preprocessed_query