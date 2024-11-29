import numpy as np

num_rows = 3
num_cols = 4
actions = ['up', 'down', 'left', 'right']
transition_probs = {
    'up': [0.8, 0.1, 0.05, 0.05],
    'down': [0.1, 0.8, 0.05, 0.05],
    'left': [0.05, 0.05, 0.8, 0.1],
    'right': [0.05, 0.05, 0.1, 0.8]
}

def get_reward(state, next_state, reward_default):
    if next_state == (0, 3): 
        return 1
    elif next_state == (0, 2):  
        return -1
    return reward_default

def value_iteration(reward_default, discount_factor=0.9, threshold=1e-6):
    value_function = np.zeros((num_rows, num_cols))
    while True:
        delta = 0
        for i in range(num_rows):
            for j in range(num_cols):
                if (i, j) == (0, 3) or (i, j) == (0, 2):
                    continue  
                old_value = value_function[i, j]
                new_value = float('-inf')
                for action in actions:
                    expected_value = 0
                    for p, next_i, next_j in zip(transition_probs[action],
                                                 [i - 1, i + 1, i, i],
                                                 [j, j, j - 1, j + 1]):
                        if 0 <= next_i < num_rows and 0 <= next_j < num_cols:
                            next_state = (next_i, next_j)
                        else:
                            next_state = (i, j) 
                        reward = get_reward((i, j), next_state, reward_default)
                        expected_value += p * (reward + discount_factor * value_function[next_state[0], next_state[1]])
                    new_value = max(new_value, expected_value)
                value_function[i, j] = new_value
                delta = max(delta, abs(old_value - new_value))
        if delta < threshold:
            break
    return value_function

reward_functions = [-2, 0.1, 0.02, 1]
for reward_default in reward_functions:
    print(f"Reward function: r(s) = {reward_default}")
    value_function = value_iteration(reward_default)
    print("Value function:")
    print(np.round(value_function, 2))
    print()
