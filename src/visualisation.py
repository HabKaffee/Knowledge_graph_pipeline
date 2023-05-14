from pyvis.network import Network
from tqdm import tqdm

def visualise_graph(triples, toggle_physics=True):
    net = Network(height='1300px',
                  width='100%',
                  bgcolor='#222222',
                  font_color='white',
                  notebook=True,
                  cdn_resources = 'local')
    with tqdm(triples, desc="Build Knowledge graph") as progress_bar:
        for triple in triples:
            net.add_node(triples.get(triple)[0], triples.get(triple)[0], title = triples.get(triple)[0])
            net.add_node(triples.get(triple)[2], triples.get(triple)[2], title = triples.get(triple)[2])
            net.add_edge(triples.get(triple)[0], triples.get(triple)[2], title = triples.get(triple)[1])
            progress_bar.update()
            progress_bar.refresh()
        progress_bar.close()
    net.toggle_physics(toggle_physics)
    net.show('KG.html')
