import numpy as np

def binary_bandit_a(action):
    p = [0.1, 0.2]
    return 1 if np.random.rand() < p[action] else 0

def binary_bandit_b(action):
    p = [0.8, 0.9]
    return 1 if np.random.rand() < p[action] else 0

num_trials = 10000
epsilon = 0.1
num_bandits = 2

Q = np.zeros(num_bandits)
N = np.zeros(num_bandits)
total_reward = 0

for trial in range(num_trials):
    if np.random.rand() < epsilon:
        action = np.random.randint(num_bandits)
    else:
        action = np.argmax(Q)

    if action == 0:
        reward = binary_bandit_a(action)
    else:
        reward = binary_bandit_b(action)

    total_reward += reward
    N[action] += 1
    Q[action] += (reward - Q[action]) / N[action]

print('Estimated values of bandits:', Q)
print('Total reward over trials:', total_reward)
