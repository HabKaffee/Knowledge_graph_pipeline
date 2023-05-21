from pyvis.network import Network
from tqdm import tqdm

def visualise_graph(triples, to_display = 1000, toggle_physics=True):
    net = Network(height='1300px',
                  width='100%',
                  bgcolor='#222222',
                  font_color='white',
                  notebook=True,
                  cdn_resources = 'local')
    triples = triples[:to_display]
    with tqdm(triples, desc="Build Knowledge graph") as progress_bar:
        for idx, triple in enumerate(triples):
            if isinstance(triples, list):
                net.add_node(triples[idx]['subject'], triples[idx]['subject'], title = triples[idx]['subject'])
                net.add_node(triples[idx]['object'], triples[idx]['object'], title = triples[idx]['object'])
                net.add_edge(triples[idx]['subject'], triples[idx]['object'], title = triples[idx]['relation'])
            else:
                raise RuntimeError("Unsopported type to build knowledge graph was passed\n"+\
                                   "Use utilities.dict_to_json_array fuction before\n")
            progress_bar.update()
            progress_bar.refresh()
        progress_bar.close()
    net.toggle_physics(toggle_physics)
    net.show('KG.html')
