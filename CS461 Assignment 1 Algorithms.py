from collections import defaultdict, deque
import heapq
import time
import resource

# Read adjacency list from txt file
def read_adjacency_list(file_path):
    adjacency_list = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            cities = line.strip().split()
            adjacency_list[cities[0]].extend(cities[1:])
            for city in cities[1:]:
                adjacency_list[city].append(cities[0])
    return adjacency_list

# Brute-force breadth-first search
def bfs(adj_list, start, end):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        visited.add(current)
        for neighbor in adj_list[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

# Brute-force depth-first search
def dfs(adj_list, start, end):
    visited = set()

    def dfs_helper(current, path):
        if current == end:
            return path
        visited.add(current)
        for neighbor in adj_list[current]:
            if neighbor not in visited:
                new_path = dfs_helper(neighbor, path + [neighbor])
                if new_path:
                    return new_path
        return None

    return dfs_helper(start, [start])

# Brute-force iterative deepening depth-first search
def iddfs(adj_list, start, end):
    depth = 0
    while True:
        result = dls(adj_list, start, end, depth)
        if result:
            return result
        depth += 1

def dls(adj_list, start, end, depth):
    visited = set()

    def dls_helper(current, path, depth):
        if depth == 0 and current == end:
            return path
        if depth > 0:
            visited.add(current)
            for neighbor in adj_list[current]:
                if neighbor not in visited:
                    new_path = dls_helper(neighbor, path + [neighbor], depth - 1)
                    if new_path:
                        return new_path
        return None

    return dls_helper(start, [start], depth)

# Heuristic best-first search
def best_first_search(adj_list, start, end):
    heap = [(0, start, [start])]
    visited = set()

    while heap:
        _, current, path = heapq.heappop(heap)
        if current == end:
            return path
        visited.add(current)
        for neighbor in adj_list[current]:
            if neighbor not in visited:
                heapq.heappush(heap, (0, neighbor, path + [neighbor]))

# Heuristic A* search
def a_star(adj_list, start, end, heuristic):
    heap = [(0, start, [start])]
    visited = set()

    while heap:
        _, current, path = heapq.heappop(heap)
        if current == end:
            return path
        visited.add(current)
        for neighbor in adj_list[current]:
            if neighbor not in visited:
                heapq.heappush(heap, (len(path) + heuristic[neighbor], neighbor, path + [neighbor]))

# Read city coordinates from csv file
def read_city_coordinates(file_path):
    city_coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            city, lat, lon = line.strip().split(',')
            city_coordinates[city] = (float(lat), float(lon))
    return city_coordinates

# Calculate Euclidean distance between two cities based on their coordinates
def euclidean_distance(city1, city2, city_coordinates):
    lat1, lon1 = city_coordinates[city1]
    lat2, lon2 = city_coordinates[city2]
    return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5

# Calculate total distance of the path
def calculate_total_distance(path, city_coordinates):
    total_distance = 0
    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i + 1]
        total_distance += euclidean_distance(city1, city2, city_coordinates)
    return total_distance

# Main function
def main():
    # Read adjacency list and city coordinates
    adjacency_list = read_adjacency_list('Adjacencies.txt')
    city_coordinates = read_city_coordinates('coordinates.csv')

    while True:
        # User inputs with input validation
        while True:
            start_city = input("Enter the start city: ").strip()
            if start_city in adjacency_list:
                break
            else:
                print("Invalid city name. Please enter a valid city.")
        
        while True:
            end_city = input("Enter the end city: ").strip()
            if end_city in adjacency_list:
                break
            else:
                print("Invalid city name. Please enter a valid city.")

        # Heuristic for A* search (Euclidean distance between cities)
        heuristic = {}
        for city in adjacency_list.keys():
            heuristic[city] = euclidean_distance(city, end_city, city_coordinates)

        # Select search method
        search_method = input("Select search method (BFS, DFS, IDDFS, BEST_FIRST, A_STAR): ").strip().upper()

        start_time = time.time()

        if search_method == "BFS":
            path = bfs(adjacency_list, start_city, end_city)
        elif search_method == "DFS":
            path = dfs(adjacency_list, start_city, end_city)
        elif search_method == "IDDFS":
            path = iddfs(adjacency_list, start_city, end_city)
        elif search_method == "BEST_FIRST":
            path = best_first_search(adjacency_list, start_city, end_city)
        elif search_method == "A_STAR":
            path = a_star(adjacency_list, start_city, end_city, heuristic)
        else:
            print("Invalid search method. Please try again.")
            continue

        end_time = time.time()
        total_time = end_time - start_time

        if path:
            total_distance = calculate_total_distance(path, city_coordinates)
            print("Path:", path)
            print("Total Distance:", total_distance)
            print("Total Time:", total_time, "seconds")
            print("Memory Used:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, "KB")
        else:
            print("No path found.")

        # Input validation for trying another search method
        while True:
            choice = input("Do you want to try another search method? (yes/no): ").strip().lower()
            if choice in ["yes", "no"]:
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        
        if choice != "yes":
            print("SEE YA!")
            break

if __name__ == "__main__":
    main()