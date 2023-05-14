import re
import string
import json
import pandas as pd
import numpy as np
import tqdm

common_abbreviations = {
    "куб." : "кубический",
    "тыс." : "тысяч(а)",
    "прим. ред." : "примечание редакции",
    "м." : "метр",
    "га." : "гектар",
    "кв." : "квадратных",
    "руб." : "рублей",
    "г." : "год(а)",
    "т.е." : "то есть"
}

def load_from_file(path_to_data:str):
    df = pd.DataFrame()
    with open(path_to_data, 'r', encoding='utf-8') as f:
        file = json.load(f)
        df = pd.DataFrame(file.get('catalog'))
    return df


def preprocess_data(corpus):
    progress_bar = tqdm.tqdm(range(14), desc="Preprocess data")
    
    ad_at_end = r'Подписывайтесь на наши страницы в *соцсетях\s?[:.] .*.'
    exclude_symbols = ''.join(['№', '«', 'ђ', '°', '±', '‚', 'ћ', '‰', '…', '»', 'ѓ', 'µ', '·', 'ґ', 'њ', 'ї', 'џ', 'є', '‹',
                            '‡', '†', '¶', 'ќ', '€', '“', 'ў', '§', '„', '”', '\ufeff', '’', 'љ', '›', '•', '—', '‘', 
                            '\x7f', '\xad', '¤', '\xa0', '\u200b', '–'])
    regex_symb = re.compile('[%s]' % re.escape(exclude_symbols))
    regex_struct = re.compile('[%s]' % string.printable + string.whitespace)
    
    corpus = [re.sub(r'<p.*>.*<\/p>', '', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    
    corpus = [re.sub(ad_at_end, "", doc).strip() for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()

    corpus = [re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()

    corpus = [re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()

    corpus = [re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    
    corpus = np.asarray([doc.strip().strip('\t').replace('\n', '') for doc in corpus])
    progress_bar.update(1)
    progress_bar.refresh()
    
    for abbriviation in common_abbreviations.keys():
        corpus = [doc.replace(abbriviation, common_abbreviations.get(abbriviation)) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()

    spaces_punct = {ord(el) : f" {el} " for el in string.punctuation}
    corpus = [doc.translate(spaces_punct) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    
    corpus = [re.sub(r' +', ' ', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    
    corpus = [re.sub(r'([a-zA-Z]+) \.', r'\1.', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()

    corpus = [re.sub(r'([А-Я]) \. ([А-Я]) \. ([А-я]+)', r'\1. \2. \3', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()

    corpus = [regex_symb.sub(' ', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    
    corpus = [regex_struct.sub('', doc) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    
    corpus = [re.sub(r' +', ' ', doc.strip()) for doc in corpus]
    progress_bar.update(1)
    progress_bar.refresh()
    progress_bar.close()
    sentenses_in_corpus = []
    
    with tqdm.tqdm(corpus, desc="Split to sentences") as progress_bar_split:
        for text in corpus:
            sentenses_in_corpus.extend(text.split(' . '))
            progress_bar_split.update()
            progress_bar_split.refresh()
        progress_bar_split.close()
    
    sentenses_in_corpus = [re.sub(r'([a-zA-Z]+)\.', r'\1 .', sentence) for sentence in sentenses_in_corpus]
    sentenses_in_corpus = [re.sub(r'([А-Я])\. ([А-Я])\. ([А-я]+)', r'\1 . \2 . \3', sentence) for sentence in sentenses_in_corpus]
    return corpus, sentenses_in_corpus



def load_preprocessed_data(path_to_data:str):
    df = load_from_file(path_to_data)
    corpus = []
    for elem in df.text.dropna():
        splitted = elem.split('\n')
        corpus += splitted
    preprocessed_corpus, preprocessed_texts = preprocess_data(corpus)
    return preprocessed_corpus, preprocessed_texts
