# graph.py
import json
import os

class CityGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.closed_edges = set()  # Уақытша жабылған жолдар тізімі

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = {}

    def remove_node(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for neighbors in self.adjacency_list.values():
                if node in neighbors:
                    del neighbors[node]

    def add_edge(self, u, v, distance, time_cost):
        if distance < 0 or time_cost < 0:
            raise ValueError("Салмақ теріс мән болмауы керек!")
        
        self.add_node(u)
        self.add_node(v)
        
        # Бағытталмаған граф болғандықтан екі жағына да қосамыз
        self.adjacency_list[u][v] = {"distance": distance, "time": time_cost}
        self.adjacency_list[v][u] = {"distance": distance, "time": time_cost}

    def remove_edge(self, u, v):
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            del self.adjacency_list[u][v]
        if v in self.adjacency_list and u in self.adjacency_list[v]:
            del self.adjacency_list[v][u]

    def update_edge_weight(self, u, v, weight_type, new_weight):
        if new_weight < 0:
            raise ValueError("Салмақ теріс мән болмауы керек!")
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            self.adjacency_list[u][v][weight_type] = new_weight
            self.adjacency_list[v][u][weight_type] = new_weight

    def close_edge(self, u, v):
        self.closed_edges.add((u, v))
        self.closed_edges.add((v, u))

    def open_all_edges(self):
        self.closed_edges.clear()

    def save_to_json(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.adjacency_list, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.adjacency_list = json.load(f)
