# main.py
from graph import CityGraph
from dijkstra import dijkstra
from visualization import visualize_city_graph

def init_default_data(graph):
    # Тапсырмадағы 15 төбе және 30 қабырға (Екі еселенген салмақ жүйесі: distance, time)
    edges_data = [
        ('A', 'B', 4, 5), ('A', 'C', 2, 3), ('B', 'C', 1, 2), ('B', 'D', 5, 4),
        ('C', 'E', 7, 6), ('C', 'F', 4, 5), ('D', 'E', 2, 2), ('D', 'G', 6, 8),
        ('E', 'F', 1, 1), ('E', 'H', 3, 2), ('F', 'H', 5, 4), ('F', 'I', 8, 7),
        ('G', 'H', 2, 3), ('G', 'J', 7, 6), ('H', 'I', 2, 3), ('H', 'K', 6, 5),
        ('I', 'L', 4, 3), ('I', 'M', 9, 8), ('J', 'K', 1, 1), ('J', 'N', 8, 9),
        ('K', 'L', 3, 2), ('K', 'N', 5, 4), ('L', 'M', 2, 3), ('L', 'O', 7, 8),
        ('M', 'O', 3, 2), ('N', 'O', 4, 3), ('B', 'F', 9, 10), ('E', 'K', 8, 7),
        ('C', 'H', 10, 12), ('G', 'N', 6, 5)
    ]
    for u, v, dist, t_cost in edges_data:
        graph.add_edge(u, v, dist, t_cost)

def run_menu():
    city = CityGraph()
    init_default_data(city)
    json_path = "data/city_graph.json"
    city.save_to_json(json_path)

    while True:
        print("\n--- АҚЫЛДЫ ҚАЛА: МАРШРУТТАУ ЖҮЙЕСІ ---")
        print("1. Ең қысқа маршрутты есептеу және визуализациялау")
        print("2. Жолды (қабырғаны) уақытша жабу/ашу")
        print("3. Жаңа қабырға қосу / Салмақ өзгерту")
        print("4. Мәліметтерді файлдан қайта жүктеу")
        print("5. Шығу")
        
        choice = input("Таңдауыңыз: ")
        
        if choice == '1':
            start = input("Бастапқы төбе (A-O): ").upper().strip()
            end = input("Соңғы төбе (A-O): ").upper().strip()
            mode = input("Режимді таңдаңыз (1 - Қашықтық, 2 - Уақыт): ").strip()
            mode_str = "time" if mode == '2' else "distance"
            
            if start == end:
                print("⚠️ Қате: Бастапқы және соңғы нүкте тең!")
                continue
                
            path, total_weight, visited, exec_time = dijkstra(city, start, end, mode=mode_str)
            
            if not path or total_weight == float('inf'):
                print(f"❌ '{start}' және '{end}' арасында маршрут табылмады немесе жол жабық!")
                visualize_city_graph(city, shortest_path=[], mode=mode_str)
            else:
                print(f"\n✅ ОҢТАЙЛЫ МАРШРУТ ТАБЫЛДЫ ({mode_str.upper()} бойынша):")
                print(f"-> Бағыт: {' -> '.join(path)}")
                print(f"-> Жалпы шығын (салмақ): {total_weight}")
                print(f"-> Қаралған төбелер саны: {visited}")
                print(f"-> Алгоритм орындалу уақыты: {exec_time:.6f} сек")
                visualize_city_graph(city, shortest_path=path, mode=mode_str)
                
        elif choice == '2':
            print("1. Жолды жабу")
            print("2. Барлық жолдарды қайта ашу")
            sub = input("Таңдау: ")
            if sub == '1':
                u = input("Төбе 1: ").upper().strip()
                v = input("Төбе 2: ").upper().strip()
                city.close_edge(u, v)
                print(f"⛔ {u}–{v} арасындағы жол уақытша жабылды.")
            else:
                city.open_all_edges()
                print("🟢 Барлық жолдар ашылды.")
                
        elif choice == '3':
            u = input("Төбе 1: ").upper().strip()
            v = input("Төбе 2: ").upper().strip()
            try:
                d = float(input("Қашықтық (distance): "))
                t = float(input("Уақыт (time): "))
                city.add_edge(u, v, d, t)
                city.save_to_json(json_path)
                print("✨ Қабырға сәтті қосылды/жаңартылды және JSON-ға сақталды.")
            except ValueError as e:
                print(f"⚠️ Қате енгізу: {e}")
                
        elif choice == '4':
            city.load_from_json(json_path)
            print("📥 Деректер JSON файлынан қайта жүктелді.")
        elif choice == '5':
            break

if __name__ == "__main__":
    run_menu()
