import numpy as np
import csv
from datetime import datetime
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt

# Function to preprocess financial data from a CSV file
def preprocess_financial_data(file_path):
    data = []
    
    # Read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        # Ensure the required columns are present
        if 'Date' not in reader.fieldnames or 'Adj Close' not in reader.fieldnames:
            raise ValueError("The CSV file must contain 'Date' and 'Adj Close' columns.")
        
        for row in reader:
            # Convert date to a standard format and adjusted close to a float
            date = datetime.strptime(row['Date'], '%d-%m-%Y')  # Adjusted to handle 'DD-MM-YYYY'
            adj_close = float(row['Adj Close'])
            data.append({'Date': date, 'Adj Close': adj_close})
    
    # Calculate daily returns
    for i in range(1, len(data)):
        prev_close = data[i - 1]['Adj Close']
        curr_close = data[i]['Adj Close']
        daily_return = (curr_close - prev_close) / prev_close
        data[i]['DailyReturn'] = daily_return
    
    # Remove the first entry (no return value available)
    data = data[1:]
    
    return data

# Fit Gaussian HMM to the returns data
def fit_gaussian_hmm(data, n_states=2):
    # Prepare the data (daily returns)
    returns = np.array([d['DailyReturn'] for d in data]).reshape(-1, 1)
    
    # Initialize and fit the HMM
    model = GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=1000)
    model.fit(returns)
    
    # Predict the hidden states
    hidden_states = model.predict(returns)
    
    return model, hidden_states

# Analyze the model parameters (means and variances of hidden states)
def analyze_model_parameters(model):
    for i in range(model.n_components):
        print(f"Hidden State {i}:")
        print(f"  Mean: {model.means_[i]}")
        print(f"  Variance: {np.diag(model.covars_[i])}\n")

# Visualize the hidden states and returns data
def plot_results(data, hidden_states):
    dates = [d['Date'] for d in data]
    returns = [d['DailyReturn'] for d in data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, returns, label='Daily Returns')
    
    # Mark the hidden states with different colors
    for i in range(len(hidden_states)):
        if hidden_states[i] == 0:
            plt.plot(dates[i], returns[i], 'ro', label='State 0 (High Volatility)' if i == 0 else "")
        elif hidden_states[i] == 1:
            plt.plot(dates[i], returns[i], 'go', label='State 1 (Low Volatility)' if i == 0 else "")
    
    plt.title("Hidden States of the Financial Market (HMM)")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Visualize the transition matrix
def plot_transition_matrix(model):
    transition_matrix = model.transmat_
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(transition_matrix, cmap='Blues')
    fig.colorbar(cax)
    ax.set_title("Transition Matrix")
    ax.set_xlabel("From State")
    ax.set_ylabel("To State")
    plt.xticks(np.arange(model.n_components), np.arange(model.n_components))
    plt.yticks(np.arange(model.n_components), np.arange(model.n_components))
    plt.show()

# Parameters
input_file = "AAPL_historical_data.csv"  # Replace with your downloaded CSV file name

# Process financial data
data = preprocess_financial_data(input_file)

# Fit HMM and analyze
model, hidden_states = fit_gaussian_hmm(data, n_states=2)
analyze_model_parameters(model)

# Plot the results
plot_results(data, hidden_states)

# Plot the transition matrix
plot_transition_matrix(model)
