import re
import string
import json
import pandas as pd
import numpy as np


def load_from_file(path_to_data:str):
    df = pd.DataFrame()
    with open(path_to_data, 'r', encoding='utf-8') as f:
        file = json.load(f)
        df = pd.DataFrame(file.get('catalog'))
    return df

def preprocess_data(corpus):
    ad_at_end = r'Подписывайтесь на наши страницы в соцсетях: .*.'
    exclude_symbols = ''.join(['№', '«', 'ђ', '°', '±', '‚', 'ћ', '‰', '…', '»', 'ѓ', 'µ', '·', 'ґ', 'њ', 'ї', 'џ', 'є', '‹',
                            '‡', '†', '¶', 'ќ', '€', '“', 'ў', '§', '„', '”', '\ufeff', '’', 'љ', '›', '•', '—', '‘', 
                            '\x7f', '\xad', '¤', '\xa0', '\u200b', '–'])
    # regex_digit = re.compile('[%s]' % re.escape(string.digits))
    regex_symb = re.compile('[%s]' % re.escape(exclude_symbols))
    regex_struct = re.compile('[%s]' % string.printable + string.whitespace)
    spaces_punct = {ord(el) : f" {el} " for el in string.punctuation}
    corpus = [re.sub(r'<p.*>.*<\/p>', '', doc) for doc in corpus]
    corpus = [re.sub(ad_at_end, "", doc).strip() for doc in corpus]
    
    corpus = [re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', doc) for doc in corpus]
    corpus = np.asarray([doc.strip().strip('\t').replace('\n', '') for doc in corpus])
    corpus = [re.sub(r' +', ' ', doc) for doc in corpus]
    corpus = [doc.translate(spaces_punct) for doc in corpus]
    # corpus = [regex_digit.sub('', doc) for doc in corpus]
    corpus = [regex_symb.sub(' ', doc) for doc in corpus]
    corpus = [regex_struct.sub('', doc) for doc in corpus]
    corpus = [re.sub(' +', ' ', doc.strip()) for doc in corpus]
    
    sentenses_in_corpus = []
    # with open("test.txt", 'w') as f:
    #     f.write(' '.join(el for el in corpus))
    for text in corpus:
        sentenses_in_corpus.extend(text.split('. '))
    return corpus, sentenses_in_corpus



def load_preprocessed_data(path_to_data:str):
    df = load_from_file(path_to_data)
    corpus, texts = [], []
    for elem in df.text.dropna():
        splitted = elem.split('\n')
        corpus += splitted
    preprocessed_corpus, preprocessed_texts = preprocess_data(corpus)
    return preprocessed_corpus, preprocessed_texts
