import numpy as np

class HopfieldEightRook:
    def __init__(self, size=8, alpha=10, beta=10):
        self.size = size  # Chessboard size (8x8)
        self.alpha = alpha  # Row constraint weight
        self.beta = beta  # Column constraint weight
        self.state = np.random.choice([0, 1], size=(size, size)).astype(float)  # Initialize state as float

    def energy(self):
        row_constraint = np.sum((np.sum(self.state, axis=1) - 1)**2)  # Row sum constraint
        col_constraint = np.sum((np.sum(self.state, axis=0) - 1)**2)  # Column sum constraint
        return self.alpha * row_constraint + self.beta * col_constraint

    def update_state(self, steps=1000):
        for step in range(steps):  # Define step here for iteration
            # Loop through each row and column
            for i in range(self.size):
                # Ensure that each row has exactly one rook
                row_sum = np.sum(self.state[i, :])
                if row_sum != 1:
                    self.state[i, :] = 0  # Reset the row to zero
                    self.state[i, np.random.randint(self.size)] = 1  # Randomly place a rook in this row

                # Ensure that each column has exactly one rook
                col_sum = np.sum(self.state[:, i])
                if col_sum != 1:
                    self.state[:, i] = 0  # Reset the column to zero
                    self.state[np.random.randint(self.size), i] = 1  # Randomly place a rook in this column

            # Apply binary threshold to simulate neurons
            self.state = np.clip(self.state, 0, 1)

    def get_solution(self):
        return self.state.astype(int)  # Convert to integer for final output

# Initialize and solve the Eight-Rook problem
eight_rook_solver = HopfieldEightRook()
eight_rook_solver.update_state()
solution = eight_rook_solver.get_solution()

print("Solved Eight-Rook Board:")
print(solution)
