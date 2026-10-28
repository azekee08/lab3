# visualization.py
import networkx as nx
import matplotlib.pyplot as plt

def visualize_city_graph(graph_obj, shortest_path=None, mode="distance"):
    plt.figure(figsize=(12, 10))
    G = nx.Graph()

    # Жүйені құру
    for u, neighbors in graph_obj.adjacency_list.items():
        for v, weights in neighbors.items():
            if not G.has_edge(u, v) and not G.has_edge(v, u):
                # Жабылған жолдарды анықтау
                is_closed = (u, v) in graph_obj.closed_edges
                G.add_edge(u, v, weight=weights[mode], closed=is_closed)

    # Төбелердің орналасу алгоритмі (көрнекі болуы үшін)
    pos = nx.spring_layout(G, seed=42)

    # 1. Барлық қабырғалар мен төбелерді салу
    standard_edges = [(u, v) for u, v, d in G.edges(data=True) if not d['closed']]
    closed_edges = [(u, v) for u, v, d in G.edges(data=True) if d['closed']]

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=600)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Стандартты жолдар (сұр түс)
    nx.draw_networkx_edges(G, pos, edgelist=standard_edges, width=1.5, edge_color='gray')
    # Жабылған жолдар (қызыл үзік сызық)
    nx.draw_networkx_edges(G, pos, edgelist=closed_edges, width=2, edge_color='red', style='dashed')

    # 2. Ең қысқа маршрутты ерекшелеп бояу (Қалың жасыл сызық)
    if shortest_path and len(shortest_path) > 1:
        path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4.5, edge_color='green')
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='lightgreen', node_size=700)

    # 3. Салмақтарды жазу
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        label = f"{d['weight']}"
        if d['closed']:
            label += " (X)"
        edge_labels[(u, v)] = label
        
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title(f"Ақылды қала маршруттар жүйесі ({mode.upper()} бойынша оңтайландыру)", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
