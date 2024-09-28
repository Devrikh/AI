import random
import math
from collections import defaultdict


cities = [
    'Jaipur', 'Jodhpur', 'Udaipur', 'Jaisalmer', 'Mount Abu', 'Bikaner',
    'Ajmer', 'Pushkar', 'Alwar', 'Bharatpur', 'Chittorgarh', 'Ranthambore',
    'Bundi', 'Kota', 'Kumbhalgarh', 'Shekhawati', 'Barmer', 'Neemrana',
    'Nathdwara', 'Pali'
]

graph = {
    'Jaipur': {'Ajmer': 135, 'Alwar': 151, 'Bikaner': 334, 'Jodhpur': 600, 'Udaipur': 660, 'Mount Abu': 650},
    'Jodhpur': {'Pali': 75, 'Barmer': 200, 'Udaipur': 250, 'Jaipur': 600},
    'Udaipur': {'Kumbhalgarh': 84, 'Nathdwara': 48, 'Chittorgarh': 117, 'Jaipur': 660, 'Jodhpur': 250},
    'Jaisalmer': {'Barmer': 153, 'Jodhpur': 500},
    'Mount Abu': {'Udaipur': 163, 'Jaipur': 650},
    'Bikaner': {'Shekhawati': 226, 'Jaipur': 334},
    'Ajmer': {'Pushkar': 15, 'Jaipur': 135},
    'Pushkar': {'Neemrana': 210, 'Ajmer': 15},
    'Alwar': {'Neemrana': 71, 'Bharatpur': 116, 'Jaipur': 151},
    'Bharatpur': {'Ranthambore': 201, 'Alwar': 116},
    'Chittorgarh': {'Kota': 182, 'Bundi': 153, 'Udaipur': 117},
    'Ranthambore': {'Bundi': 145, 'Bharatpur': 201},
    'Bundi': {'Kota': 35, 'Chittorgarh': 153, 'Ranthambore': 145},
    'Kota': {'Nathdwara': 235, 'Bundi': 35, 'Chittorgarh': 182},
    'Kumbhalgarh': {'Pali': 100, 'Udaipur': 84},
    'Shekhawati': {'Neemrana': 150, 'Bikaner': 226},
    'Barmer': {'Jaisalmer': 153, 'Jodhpur': 200},
    'Neemrana': {'Pushkar': 210, 'Alwar': 71, 'Shekhawati': 150},
    'Nathdwara': {'Udaipur': 48, 'Kota': 235},
    'Pali': {'Jodhpur': 75, 'Kumbhalgarh': 100}
}


distances = defaultdict(lambda: defaultdict(lambda: float('inf')))

for city in cities:
    distances[city][city] = 0  
    for neighbor, distance in graph.get(city, {}).items():
        distances[city][neighbor] = distance

for k in cities:
    for i in cities:
        for j in cities:
            if distances[i][j] > distances[i][k] + distances[k][j]:
                distances[i][j] = distances[i][k] + distances[k][j]

print("Distance Matrix:")
for city in cities:
    print(f"{city}: {dict(distances[city])}")


def calculate_tour_cost(tour, distances):
    total_cost = 0
    for i in range(len(tour)):
        current_city = tour[i]
        next_city = tour[(i + 1) % len(tour)]  
        cost = distances[current_city][next_city]
        total_cost += cost
        
        
        print(f"Calculating cost from {current_city} to {next_city}: {cost}")
        
    return total_cost


def simulated_annealing(cities, distances, initial_temp, cooling_rate):
    current_solution = cities[:]
    random.shuffle(current_solution)
    current_cost = calculate_tour_cost(current_solution, distances)

    temp = initial_temp
    best_solution = current_solution[:]
    best_cost = current_cost

    while temp > 1:
        new_solution = current_solution[:]
        i, j = random.sample(range(len(cities)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

        new_cost = calculate_tour_cost(new_solution, distances)

        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
            current_solution = new_solution[:]
            current_cost = new_cost

            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost

        temp *= cooling_rate

    return best_solution, best_cost

initial_temp = 10000
cooling_rate = 0.995


best_tour, best_cost = simulated_annealing(cities, distances, initial_temp, cooling_rate)


print("Best tour:", best_tour)
print("Total cost:", best_cost)