import numpy as np

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size  # Total number of neurons
        self.weights = np.zeros((size, size))  # Initialize weight matrix

    def train(self, patterns):
        # Train using Hebbian learning
        for pattern in patterns:
            p = pattern.reshape(-1, 1)
            self.weights += np.dot(p, p.T)  # Update weights
        np.fill_diagonal(self.weights, 0)  # No self-connections
        self.weights /= len(patterns)  # Normalize by number of patterns

    def recall(self, pattern, steps=10):
        # Recall a pattern by updating neurons iteratively
        recalled_pattern = pattern.copy()
        for _ in range(steps):
            for i in range(self.size):
                net_input = np.dot(self.weights[i], recalled_pattern)
                recalled_pattern[i] = 1 if net_input >= 0 else -1  # Sign activation
        return recalled_pattern

# Create 10x10 grid patterns (100 neurons)
size = 100
patterns = [
    np.random.choice([-1, 1], size=size),  # Random binary patterns
    np.random.choice([-1, 1], size=size),
]

# Train the network
hopfield = HopfieldNetwork(size)
hopfield.train(patterns)

# Test with a noisy version of a stored pattern
test_pattern = patterns[0].copy()
noise_level = 10  # Number of bits to flip
flip_indices = np.random.choice(size, noise_level, replace=False)
test_pattern[flip_indices] *= -1  # Introduce noise

# Recall and compare
recalled = hopfield.recall(test_pattern)
print("Original Pattern:\n", patterns[0].reshape(10, 10))
print("Noisy Pattern:\n", test_pattern.reshape(10, 10))
print("Recalled Pattern:\n", recalled.reshape(10, 10))
