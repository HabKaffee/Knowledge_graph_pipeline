import json
from tqdm import tqdm

def load_triples(path_to_file):
    triples = []
    with open(path_to_file, 'r', encoding="utf-8") as file:
        triples = json.load(file)
    return triples


def dict_to_json_array(triples:dict):
    triples_json_array = []
    with tqdm(triples, desc='Move triples from dictionary to json format') as progress_bar:
        for key in triples.keys():
            triples_json = {
                "sentence" : key.text,
                "subject" : triples.get(key)[0],
                "relation" : str(triples.get(key)[1]),
                "object" : triples.get(key)[2]
            }
            triples_json_array.append(triples_json)
            progress_bar.update()
            progress_bar.refresh()
        progress_bar.close()
    return triples_json_array


def dump_triples_to_file(path:str, triples:dict):
    with open(path, 'w', encoding="utf-8") as file:
        triples_json_array = dict_to_json_array(triples)
        json_string = json.dumps(triples_json_array, indent=2, ensure_ascii=False)
        file.write(json_string)
