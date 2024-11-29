import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Example data: dates and returns
df = pd.DataFrame({
    'Date': pd.date_range(start='2020-01-01', periods=100),
    'Returns': [0.01 * (x % 5) for x in range(100)]  # Example return values
})

# Hidden states inferred by HMM (e.g., 3 hidden states)
hidden_states = np.array([x % 3 for x in range(100)])  # Example hidden states (0, 1, 2)

# Plot the returns with color-coding based on hidden states
plt.figure(figsize=(10, 6))
for i in range(3):  # For each hidden state
    # Select the data points where the hidden state matches `i`
    state_data = df[hidden_states == i]
    plt.plot(state_data['Date'], state_data['Returns'], label=f'State {i}', color=f'C{i}')

plt.xlabel('Date')
plt.ylabel('Returns')
plt.title('Stock Returns with Color-Coding by Hidden States')
plt.legend()
plt.show()
