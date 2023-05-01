import spacy
import os
from tqdm.auto import tqdm
# import cupy
# import cupyx
# import cupy.cuda
# from cupy.cuda.compiler import compile_with_cache
# import torch


from src.preprocessing import load_preprocessed_data

def do_ner():
    activated = spacy.require_gpu()
    if not activated:
        print("GPU not used. Exiting...")
        exit(1)
    else:
        print("GPU used")
    lang_model = spacy.load('ru_core_news_lg')
    preprocessed_corpus, preprocessed_texts = load_preprocessed_data(f'{os.getcwd()}/data/result.json')
    # test_corpus = ['Эта книга адресована всем, кто изучает русский язык. \
    #                 Но состоит она не из правил, упражнений и учебных текстов. \
    #                 Для этого созданы другие замечательные учебники. \
    #                 У этой книги совсем иная задача. \
    #                 Она поможет вам научиться не только разговаривать, но и размышлять по-русски.\
    #                 Книга, которую вы держите в руках, составлена из афоризмов и размышлений великих мыслителей, писателей, поэтов, философов и общественных деятелей различных эпох. \
    #                 Их мысли - о тех вопросах, которые не перестают волновать человечество.\
    #                 Вы можете соглашаться или не соглашаться с тем, что прочитаете в этой книге. \
    #                 Возможно, вам покажется, что какие-то мысли уже устарели. \
    #                 Но вы должны обязательно подумать и обосновать, почему вы так считаете. \
    #                 А еще вы узнаете и почувствуете, как прекрасно звучат слова любви, сострадания, мудрости и доброты на русском языке.']
    corpus_after_lm = [lang_model(doc) for doc in preprocessed_corpus]
    named_entities = {doc : [] for doc in corpus_after_lm}
    for text in tqdm(corpus_after_lm):
        for named_entity in text.ents:
            named_entities[text].append([named_entity, named_entity.label_])
    # for key, value in named_entities.items():
    #     print(key, value)
    return named_entities

def do_pos():
    activated = spacy.require_gpu()
    if not activated:
        print("GPU not used. Exiting...")
        exit(1)
    else:
        print("GPU used")
    lang_model = spacy.load('ru_core_news_lg')
    preprocessed_corpus, preprocessed_texts = load_preprocessed_data(f'{os.getcwd()}/data/result.json')
    # test_corpus = ['Эта книга адресована всем, кто изучает русский язык. \
    #                 Но состоит она не из правил, упражнений и учебных текстов. \
    #                 Для этого созданы другие замечательные учебники. \
    #                 У этой книги совсем иная задача. \
    #                 Она поможет вам научиться не только разговаривать, но и размышлять по-русски.\
    #                 Книга, которую вы держите в руках, составлена из афоризмов и размышлений великих мыслителей, писателей, поэтов, философов и общественных деятелей различных эпох. \
    #                 Их мысли - о тех вопросах, которые не перестают волновать человечество.\
    #                 Вы можете соглашаться или не соглашаться с тем, что прочитаете в этой книге. \
    #                 Возможно, вам покажется, что какие-то мысли уже устарели. \
    #                 Но вы должны обязательно подумать и обосновать, почему вы так считаете. \
    #                 А еще вы узнаете и почувствуете, как прекрасно звучат слова любви, сострадания, мудрости и доброты на русском языке.']
    corpus_after_lm = [lang_model(doc) for doc in preprocessed_corpus]
    pos = {doc : [] for doc in corpus_after_lm}
    for text in tqdm(corpus_after_lm):
        for token in text:
            pos[text].append([token, token.lemma_, token.pos_, token.dep_])
    # for key, value in pos.items():
    #     print(key, value)
    return pos

# if __name__ == "__main__":
#     do_ner()
#     # do_pos()
