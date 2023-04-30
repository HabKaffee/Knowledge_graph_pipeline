import spacy
import os
# import cupy
# import cupyx
# import cupy.cuda
# from cupy.cuda.compiler import compile_with_cache
# import torch


from preprocessing import load_preprocessed_data

def do_ner():
    activated = spacy.require_gpu()
    if not activated:
        print("GPU not used. Exiting...")
        exit(1)
    else:
        print("GPU used")
    lang_model = spacy.load('ru_core_news_lg')
    preprocessed_corpus, preprocessed_texts = load_preprocessed_data(f'{os.getcwd()}/data/result.json')
    # print(preprocessed_corpus[0])
    recognised_ents_list = []
    # print(preprocessed_corpus[])
    recognised_ents_list = [lang_model(doc) for doc in preprocessed_corpus[0:10]]
    for recognised_ents in recognised_ents_list:
        for named_entity in recognised_ents.ents:
            print(named_entity, named_entity.label_)

if __name__ == "__main__":
    do_ner()
