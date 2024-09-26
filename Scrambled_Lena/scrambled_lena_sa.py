import random
import math
from PIL import Image
import numpy as np

def calculate_cost(image_puzzle):
    total_cost = 0
    for row in range(512):
        for col in range(512):
            if col + 1 != 512 and (col + 1) % 128 == 0:
                total_cost += abs(int(image_puzzle[(512 * row) + col]) - int(image_puzzle[(512 * row) + col + 1]))
            if row + 1 != 512 and (row + 1) % 128 == 0:
                total_cost += abs(int(image_puzzle[(512 * row) + col]) - int(image_puzzle[(512 * (row + 1)) + col]))
    return total_cost

def swap_pieces(image_puzzle):
    idx1, idx2 = random.sample(range(16), 2)
    row1, col1 = divmod(idx1, 4)
    row2, col2 = divmod(idx2, 4)
    start_row1, start_row2 = 128 * row1, 128 * row2
    start_col1, start_col2 = 128 * col1, 128 * col2

    piece_one = []
    piece_two = []

    for i in range(128):
        for j in range(128):
            piece_one.append(image_puzzle[(512 * (start_row1 + i)) + (start_col1 + j)])
            piece_two.append(image_puzzle[(512 * (start_row2 + i)) + (start_col2 + j)])
    
    for i in range(128):
        for j in range(128):
            image_puzzle[(512 * (start_row1 + i)) + (start_col1 + j)] = piece_two[(i * 128) + j]
            image_puzzle[(512 * (start_row2 + i)) + (start_col2 + j)] = piece_one[(i * 128) + j]

    return image_puzzle

def simulated_annealing(initial_puzzle, initial_temp, cooling_rate, final_temp):
    best_cost = float('inf')
    best_state = []
    temperature = initial_temp
    current_state = initial_puzzle
    current_cost = calculate_cost(current_state)
    
    while temperature > final_temp:
        new_state = swap_pieces(current_state.copy())
        new_cost = calculate_cost(new_state)

        if new_cost < current_cost:
            current_state = new_state
            current_cost = new_cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_state = current_state.copy()
        else:
            if random.uniform(0, 1) < math.exp((current_cost - new_cost) / temperature):
                current_state = new_state
                current_cost = new_cost
        
        temperature *= cooling_rate 
    
    return best_state, best_cost


def display_image_from_text(file_path):
    pixel_values = []
    with open(file_path, 'r') as file:
        for line in file:
            pixel_values.extend(int(num) for num in line.split())

    pixel_array = np.array(pixel_values, dtype=np.uint8).reshape((512, 512))
    img = Image.fromarray(pixel_array, mode='L')
    img.show()




image_puzzle = []
with open('scrambled_lena.mat', 'r') as file:
    for line in file:
        image_puzzle.extend(line.split())

assert len(image_puzzle) == 512 * 512, "Puzzle data does not match expected size!"

final_solution = []
best_cost = float('inf') 

for attempt in range(5):
    initial_temp = 1000
    cooling_rate = 0.99
    final_temp = 0.1
    solved_puzzle, cost = simulated_annealing(image_puzzle, initial_temp, cooling_rate, final_temp)
    
    if cost < best_cost:
        best_cost = cost
        image_puzzle = solved_puzzle.copy()
        final_solution = image_puzzle
    print(cost)

with open('ans.mat', 'w') as file:
    for item in solved_puzzle:
        file.write(f"{item}\n") 

# Write the output data
with open('ans.mat', 'w') as output_file:
    for value in final_solution:
        output_file.write(f"{value}\n") 

display_image_from_text('ans.mat')
