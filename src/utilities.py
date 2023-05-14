from tqdm import tqdm

def load_triples(path_to_file):
    triples = {}
    with open(path_to_file, 'r', encoding="utf-8") as file:
        for line in file:
            key_value = line.split(" ^ ")
            values = key_value[1].split(" | ")
            values[0] = values[0].replace("(", "")
            values[2] = values[2].replace(")", "").replace('\n', '')
            triples[key_value[0]] = (values[0], values[1], values[2])
    return triples


def dump_triples_to_file(path:str, triples:dict):
    with open(path, 'w', encoding="utf-8") as file:
        file.write("Sentence ^ (Subject | relation | object)\n")
        with tqdm(triples, desc=f'Writing data to {path}') as progress_bar:
            for key in triples.keys():
                file.write(f"{key.text} ^ ({triples.get(key)[0]} | {triples.get(key)[1]} | {triples.get(key)[2]})\n")
                progress_bar.update()
                progress_bar.refresh()
            progress_bar.close()