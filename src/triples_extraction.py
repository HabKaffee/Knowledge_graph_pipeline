import os
import spacy
from spacy.symbols import nsubj, nsubjpass, dobj, iobj, pobj, obj, obl, nmod, conj, xcomp
import textacy
from tqdm import tqdm

from src.preprocessing import load_preprocessed_data

VERB_PATTERNS = [
        [{"POS":"VERB", "DEP":"ROOT"}],
        [{"POS":"VERB"}, {"POS":"VERB"}],
        [{"POS":"AUX"}, {"POS":"VERB"}],
        [{"POS":"NOUN", "DEP":"ROOT"}],
        [{"POS":"ADJ", "DEP":"ROOT"}],
        [{"POS":"ADJ", "DEP":"ROOT"}, {"POS":"VERB"}],
        [{"POS":"VERB", "DEP":"parataxis"}],
        [{"POS":"ADV", "DEP":"ROOT"}, {"POS":"VERB"}],
    ]

NP_LABELS = set([nsubj, nsubjpass, dobj, iobj, pobj, obj, obl, nmod, conj, xcomp])

def pos_tagging():
    activated = spacy.require_gpu()
    if not activated:
        print("GPU is not used. Exiting...")
        exit(1)
    else:
        print("GPU is used")
    lang_model = spacy.load('ru_core_news_lg')
    preprocessed_corpus, preprocessed_corpus_sentences = load_preprocessed_data(f'{os.getcwd()}/data/result.json')
    corpus_after_lm = [lang_model(doc) for doc in tqdm(preprocessed_corpus_sentences, desc="Processing by language model")]
    pos = {doc : [] for doc in corpus_after_lm}
    with tqdm(corpus_after_lm, desc="Filling dictionary") as progress_bar:
        for text in corpus_after_lm:
            for token in text:
                pos[text].append([token, token.lemma_, token.pos_, token.dep_])
            progress_bar.update()
            progress_bar.refresh()
        progress_bar.close()
    return pos


def find_root_of_sentence(sentence):
    root_token = None
    for token in sentence:
        if token.dep_ == "ROOT":
            root_token = token
    return root_token


def contains_root(verb_phrase, root):
    vp_start = verb_phrase.start
    vp_end = verb_phrase.end
    return vp_start <= root.i <= vp_end if root is not None else False


def get_verb_phrases(sentence):
    root = find_root_of_sentence(sentence)
    verb_phrases = list(textacy.extract.matches.token_matches(sentence, VERB_PATTERNS))
    return [verb_phrase for verb_phrase in verb_phrases if contains_root(verb_phrase, root)]


def get_noun_chunks(sentence):
    chunks = []
    for token in sentence:
        if token.dep in NP_LABELS:
            chunks.append(' '.join(t.text for t in token.subtree))
    return chunks


def get_longest_verb_phrase(verb_phrases):
    longest_length = 0
    longest_verb_phrase = None
    for verb_phrase in verb_phrases:
        if len(verb_phrase) > longest_length:
            longest_verb_phrase = verb_phrase
            longest_length = len(verb_phrase)
    return longest_verb_phrase


def find_start_pos(sentense, noun_phrase):
    splitted_phrase = noun_phrase.split()
    splitted_sentence = sentense.text.split()
    return splitted_sentence.index(splitted_phrase[0])


def find_noun_phrase(sentence, verb_phrase, noun_phrases, side):
    for noun_phrase in noun_phrases:
        if (side == "left") and (find_start_pos(sentence, noun_phrase) < verb_phrase.start):
            return noun_phrase
        elif (side == "right") and (find_start_pos(sentence, noun_phrase) > verb_phrase.start):
            return noun_phrase


def extract_triples(sentence):
    verb_phrases = get_verb_phrases(sentence)
    noun_phrases = get_noun_chunks(sentence)
    if len(verb_phrases) == 0:
        return
    verb_phrase = get_longest_verb_phrase(verb_phrases) if len(verb_phrases) > 1 else verb_phrases[0]
    left_noun_phrase = find_noun_phrase(sentence, verb_phrase, noun_phrases, "left")
    right_noun_phrase = find_noun_phrase(sentence, verb_phrase, noun_phrases, "right")
    return (left_noun_phrase, verb_phrase, right_noun_phrase)


def clean_triples(extracted_triples):
    cleaned_triples = {}
    with tqdm(extracted_triples, desc="Clean triples") as progress_bar:
        for triple in extracted_triples:
            if all(extracted_triples.get(triple)):
                cleaned_triples[triple] = extracted_triples.get(triple)
            progress_bar.update()
            progress_bar.refresh()
        progress_bar.close()
    return cleaned_triples


def dump_triples_to_file(path:str, triples:dict):
    with open(path, 'w', encoding="utf-8") as file:
        file.write("Sentence : (Subject, relation, object)\n")
        with tqdm(triples, desc=f'Writing data to {path}') as progress_bar:
            for key in triples.keys():
                file.write(f"{key.text} : ({triples.get(key)[0], triples.get(key)[1], triples.get(key)[2]})\n")
                progress_bar.update()
                progress_bar.refresh()
            progress_bar.close()
