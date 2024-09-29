import random
import math
from PIL import Image
import numpy as np

def calculate_cost(image_data):
    total_cost = 0
    for row in range(512):
        for col in range(512):
            if col % 128 == 127 and col < 511:
                total_cost += abs(int(image_data[row * 512 + col]) - int(image_data[row * 512 + col + 1]))
            if row % 128 == 127 and row < 511:
                total_cost += abs(int(image_data[row * 512 + col]) - int(image_data[(row + 1) * 512 + col]))
    return total_cost

def swap_pieces(image_data):
    piece_idx1, piece_idx2 = random.sample(range(16), 2)
    row1, col1 = divmod(piece_idx1, 4)
    row2, col2 = divmod(piece_idx2, 4)
    
    start_r1, start_c1 = row1 * 128, col1 * 128
    start_r2, start_c2 = row2 * 128, col2 * 128

    piece_1, piece_2 = [], []
    for i in range(128):
        for j in range(128):
            piece_1.append(image_data[(start_r1 + i) * 512 + start_c1 + j])
            piece_2.append(image_data[(start_r2 + i) * 512 + start_c2 + j])

    for i in range(128):
        for j in range(128):
            image_data[(start_r1 + i) * 512 + start_c1 + j] = piece_2[i * 128 + j]
            image_data[(start_r2 + i) * 512 + start_c2 + j] = piece_1[i * 128 + j]

    return image_data

def simulated_annealing(initial_image, initial_temp, cooling_rate, final_temp):
    min_cost = float('inf')
    best_state = []
    temperature = initial_temp
    current_image = initial_image
    current_cost = calculate_cost(current_image)
    
    while temperature > final_temp:
        new_image = swap_pieces(current_image.copy())
        new_cost = calculate_cost(new_image)
        if new_cost < current_cost:
            current_image = new_image
            current_cost = new_cost
            if current_cost < min_cost:
                min_cost = current_cost
                best_state = current_image.copy()
        else:
            if random.uniform(0, 1) < math.exp((current_cost - new_cost) / temperature):
                current_image = new_image
                current_cost = new_cost
        
        temperature *= cooling_rate
    
    return best_state, min_cost


def display_image(file_path):
    pixel_values = []
    with open(file_path, 'r') as file:
        for line in file:
            pixel_values.extend(int(num) for num in line.split())
    pixel_array = np.array(pixel_values, dtype=np.uint8).reshape((512, 512))


    pixel_array = np.transpose(pixel_array)
    img = Image.fromarray(pixel_array, mode='L')
    img.show()


image_puzzle = []
with open('scrambled_lena.mat', 'r') as file:
    for line in file:
        image_puzzle.extend(line.split())
assert len(image_puzzle) == 512 * 512, "Puzzle data does not match expected size!"

final_solution = []
best_cost = float('inf') 

for i in range(5):
    initial_temp = 1000
    cooling_rate = 0.99
    final_temp = 0.1
    solved_puzzle, cost = simulated_annealing(image_puzzle, initial_temp, cooling_rate, final_temp)
    
    if cost < best_cost:
        best_cost = cost
        image_puzzle = solved_puzzle.copy()
        final_solution = image_puzzle
    print(cost)

with open('ans.mat', 'w') as output_file:
    for value in final_solution:
        output_file.write(f"{value}\n") 

display_image('ans.mat')
