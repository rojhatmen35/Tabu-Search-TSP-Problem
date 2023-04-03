import random
import numpy as np

def calculate_cost_matrix(coordinates):
    num_cities = len(coordinates)
    cost_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            cost_matrix[i][j] = np.sqrt((coordinates[j][0] - coordinates[i][0])**2 + (coordinates[j][1] - coordinates[i][1])**2)
    return cost_matrix

def tabu_search(cost_matrix, num_iterations=5000, tabu_size=15):
    num_cities = cost_matrix.shape[0]
    current_path = list(range(num_cities))
    current_cost = calculate_path_cost(current_path, cost_matrix)
    best_path = list(current_path)
    best_cost = current_cost
    tabu_list = []
    for i in range(num_iterations):
        candidate_paths = get_candidate_paths(current_path, tabu_list, tabu_size)
        candidate_costs = [calculate_path_cost(path, cost_matrix) for path in candidate_paths]
        best_candidate_idx = np.argmin(candidate_costs)
        best_candidate_path = candidate_paths[best_candidate_idx]
        best_candidate_cost = candidate_costs[best_candidate_idx]
        if best_candidate_cost < best_cost:
            best_path = list(best_candidate_path)
            best_cost = best_candidate_cost
        current_path = list(best_candidate_path)
        current_cost = best_candidate_cost
        tabu_list.append(list(best_candidate_path))
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
    return best_cost, best_path

def get_candidate_paths(path, tabu_list, tabu_size):
    candidate_paths = []
    for i in range(tabu_size*10):
        candidate_path = list(path)
        rand_pos1 = random.randint(0, len(path)-1)
        rand_pos2 = random.randint(0, len(path)-1)
        while rand_pos2 == rand_pos1:
            rand_pos2 = random.randint(0, len(path)-1)
        candidate_path[rand_pos1], candidate_path[rand_pos2] = candidate_path[rand_pos2], candidate_path[rand_pos1]
        if candidate_path not in tabu_list:
            candidate_paths.append(candidate_path)
    return candidate_paths

def calculate_path_cost(path, cost_matrix):
    cost = 0
    for i in range(len(path)-1):
        cost += cost_matrix[path[i]][path[i+1]]
    cost += cost_matrix[path[-1]][path[0]]
    return cost

# Örnek verileri kullanarak Tabu Search algoritması ile TCP problemi çözümü
# Örnek dosyaların boyutu: (5, 124, 1000, 5915, 11849)

def read_file(file_name: str) -> np.ndarray:
    data = np.loadtxt(file_name, skiprows=1)
    return data

if __name__ == '__main__':
    file_sizes = [5, 124, 1000, 5915, 11849]
    for file_size in file_sizes:
        file_names = f"{file_size}.txt"
        cost_matrix = calculate_cost_matrix(read_file(file_names))
        optimal_cost, optimal_path = tabu_search(cost_matrix)
        print("Optimal maliyet değeri:", optimal_cost)
        print("Optimal çözüm için sırası ile gidilecek nodelar (şehirler):", "->".join(str(i) for i in optimal_path))


 

