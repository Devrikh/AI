import numpy as np

def project_to_permutation(state):
    """
    Enforce the state to be a valid permutation matrix.
    Each row is mapped to a one-hot vector by setting the maximum value to 1.
    """
    projected_state = np.zeros_like(state)
    for i in range(state.shape[0]):
        max_idx = np.argmax(state[i])
        projected_state[i, max_idx] = 1
    return projected_state

class HopfieldTSP:
    def __init__(self, cities, distance_matrix, alpha=100, beta=100, gamma=1, learning_rate=0.01):
        self.N = len(cities)
        self.D = distance_matrix
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.state = self.initialize_state()

    def initialize_state(self):
        """
        Randomly initialize the state matrix and normalize to have row sums of 1.
        """
        state = np.random.uniform(0, 1, (self.N, self.N))
        state /= np.sum(state, axis=1, keepdims=True)
        return state

    def energy(self):
        """
        Calculate the energy of the current state.
        """
        row_constraint = np.sum((np.sum(self.state, axis=1) - 1) ** 2)
        col_constraint = np.sum((np.sum(self.state, axis=0) - 1) ** 2)
        shifted_state = np.roll(self.state, -1, axis=1)
        distance_sum = np.sum(self.D * shifted_state * self.state)
        return self.alpha * row_constraint + self.beta * col_constraint + self.gamma * distance_sum

    def update_state(self, steps=5000):
        """
        Update the state using gradient descent, projecting to a valid permutation at each step.
        """
        for step in range(steps):
            # Compute row and column errors
            row_error = np.sum(self.state, axis=1, keepdims=True) - 1
            col_error = np.sum(self.state, axis=0, keepdims=True) - 1

            # Compute the distance gradient
            shifted_state = np.roll(self.state, -1, axis=1)
            dist_grad = np.dot(self.D, shifted_state)

            # Combine gradients
            grad = (self.alpha * row_error +
                    self.beta * col_error +
                    self.gamma * dist_grad)

            # Update state using gradient descent
            self.state -= self.learning_rate * grad

            # Strict projection to a valid permutation matrix
            self.state = project_to_permutation(self.state)

            # Log energy and state periodically
            if step % 100 == 0:
                print(f"Step {step}, Energy: {self.energy()}")
                print(f"State at step {step}:\n{self.state}")
                print("-" * 40)

    def get_tour(self):
        """
        Extract the tour from the binary state.
        """
        tour = []
        for row in self.state:
            tour.append(np.argmax(row))
        return tour

# Example with 5 cities and a distance matrix
cities = ['A', 'B', 'C', 'D', 'E']
distance_matrix = np.array([[0, 1, 1, 4, 13],
                            [10, 0, 13, 10, 7],
                            [10, 14, 0, 15, 16],
                            [7, 18, 7, 0, 7],
                            [13, 7, 14, 3, 0]])

# Solve the TSP
tsp_solver = HopfieldTSP(cities, distance_matrix, alpha=500, beta=500, gamma=1, learning_rate=0.001)
tsp_solver.update_state(steps=5000)
tour = tsp_solver.get_tour()

print("\nDistance Matrix:\n", distance_matrix)
print("Optimal Tour (approx):", [cities[i] for i in tour])
