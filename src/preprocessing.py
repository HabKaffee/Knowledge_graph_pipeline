import pandas as pd
import numpy as np
import re
import string
from scipy.sparse import *
import json

def load_from_file(path_to_data:str):
    df = pd.DataFrame()
    with open(path_to_data, 'r', encoding='utf-8') as f:
        file = json.load(f)
        df = pd.DataFrame(file.get('catalog'))
    return df

def preprocess_data(corpus, texts):
    ad_at_end = r'Подписывайтесь на наши страницы в соцсетях: .*.'
    exclude_symbols = u''.join(['№', '«', 'ђ', '°', '±', '‚', 'ћ', '‰', '…', '»', 'ѓ', 'µ', '·', 'ґ', 'њ', 'ї', 'џ', 'є', '‹',
                            '‡', '†', '¶', 'ќ', '€', '“', 'ў', '§', '„', '”', '\ufeff', '’', 'љ', '›', '•', '—', '‘', 
                            '\x7f', '\xad', '¤', '\xa0', '\u200b', '–'])
    # regex_punct = re.compile('[%s]' % re.escape(string.punctuation).replace('.', ''))
    # regex_digit = re.compile('[%s]' % re.escape(string.digits))
    regex_symb = re.compile('[%s]' % re.escape(exclude_symbols))
    regex_struct = re.compile('[%s]' % string.printable + string.whitespace)

    corpus = [re.sub(r'<p.*>.*<\/p>', '', doc) for doc in corpus]
    corpus = [re.sub(ad_at_end, "", doc).strip() for doc in corpus]
    texts = [re.sub(ad_at_end, "", doc).strip() for doc in texts]
    
    corpus = [re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', u'', doc) for doc in corpus]
    corpus = np.asarray([doc.strip().strip('\t').replace('\n', u'') for doc in corpus])
    corpus = [re.sub(r' +', ' ', doc) for doc in corpus]
    # corpus = [regex_punct.sub('', doc) for doc in corpus]
    # corpus = [regex_digit.sub('', doc) for doc in corpus]
    corpus = [regex_symb.sub(' ', doc) for doc in corpus]
    corpus = [regex_struct.sub('', doc) for doc in corpus]
    corpus = [re.sub(' +', ' ', doc.strip()) for doc in corpus]

    #TODO: does words need to be normalized?

    return corpus, texts



def load_preprocessed_data(path_to_data:str):
    df = load_from_file(path_to_data)
    corpus, texts = [], []
    for elem in df.text.dropna():
        splitted = elem.split('\n')
        corpus += splitted
        texts += splitted
    preprocessed_corpus, preprocessed_texts = preprocess_data(corpus, texts)
    return preprocessed_corpus, preprocessed_texts
