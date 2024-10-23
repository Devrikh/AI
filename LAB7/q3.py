import random
import numpy as np

class BanditNonStat:
    def __init__(self, n_arms=10, initial_mean=0):
        self.n_arms = n_arms
        self.mean_rewards = [initial_mean] * n_arms
        self.stddev = 0.01

    def step(self):
        for i in range(self.n_arms):
            self.mean_rewards[i] += random.gauss(0, self.stddev)

    def get_reward(self, action):
        return round(random.gauss(self.mean_rewards[action], 1), 2)

    def select_action(self, epsilon):
        if random.random() < epsilon:
            return random.randint(0, self.n_arms - 1)
        else:
            return np.argmax([self.mean_rewards[i] for i in range(self.n_arms)])

def run_bandit_simulation():
    bandit = BanditNonStat()

    steps = int(input("Enter the number of steps to simulate: "))
    epsilon = 0.1

    for step in range(steps):
        action = bandit.select_action(epsilon)
        reward = bandit.get_reward(action)
        print(f"Step {step + 1}: Action {action}, Reward {reward}")
        bandit.step()

run_bandit_simulation()
