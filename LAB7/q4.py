import random

class AdaptiveEpsilonGreedyAgent:
    def __init__(self, n_actions, initial_epsilon, alpha, decay_rate):
        self.n_actions = n_actions
        self.epsilon = initial_epsilon
        self.alpha = alpha
        self.decay_rate = decay_rate
        self.q_values = [0.0] * n_actions
        self.action_counts = [0] * n_actions
        self.total_rewards = []
        self.recent_rewards = []

    def select_action(self):
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return self.q_values.index(max(self.q_values))

    def update(self, action, reward):
        self.action_counts[action] += 1
        self.q_values[action] += self.alpha * (reward - self.q_values[action])
        self.total_rewards.append(reward)
        self.recent_rewards.append(reward)

        if len(self.recent_rewards) > 100:
            avg_reward = sum(self.recent_rewards[-100:]) / 100
            if avg_reward < 0:
                self.epsilon = min(1.0, self.epsilon + 0.01)

        self.epsilon = max(0.01, self.epsilon * self.decay_rate)

def non_stationary_rewards(t):
    return random.gauss(random.uniform(0, 1) + 1, 1)

def run_experiment(n_actions, n_steps, initial_epsilon, alpha, decay_rate):
    agent = AdaptiveEpsilonGreedyAgent(n_actions, initial_epsilon, alpha, decay_rate)
    rewards = []

    for t in range(n_steps):
        action = agent.select_action()
        reward = non_stationary_rewards(t)
        agent.update(action, reward)
        rewards.append(reward)

        if t % 1000 == 0:
            print(f"Step {t}: Total Reward = {sum(rewards)}")

    return rewards, agent.q_values

n_actions = int(input("Enter the number of actions (e.g., 10): "))
n_steps = int(input("Enter the number of steps (e.g., 10000): "))
initial_epsilon = float(input("Enter the initial epsilon (e.g., 0.1): "))
alpha = float(input("Enter the alpha (step size for updating estimates, e.g., 0.1): "))
decay_rate = float(input("Enter the decay rate (e.g., 0.99): "))

rewards, q_values = run_experiment(n_actions, n_steps, initial_epsilon, alpha, decay_rate)

print("Final action-value estimates:", q_values)
