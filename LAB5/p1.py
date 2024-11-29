import csv
from datetime import datetime

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
            try:
                # Convert date to a standard format and adjusted close to a float
                date = datetime.strptime(row['Date'], '%Y-%m-%d')
                adj_close = float(row['Adj Close'])
                data.append({'Date': date, 'Adj Close': adj_close})
            except (ValueError, KeyError):
                # Skip rows with invalid data
                continue
    
    # Calculate daily returns
    for i in range(1, len(data)):
        prev_close = data[i - 1]['Adj Close']
        curr_close = data[i]['Adj Close']
        daily_return = (curr_close - prev_close) / prev_close
        data[i]['DailyReturn'] = daily_return
    
    # Remove the first entry (no return value available)
    data = data[1:]
    
    return data

# Function to save preprocessed data to a new CSV file
def save_preprocessed_data(data, output_file):
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['Date', 'Adj Close', 'DailyReturn']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            row['Date'] = row['Date'].strftime('%Y-%m-%d')  # Format date for CSV
            writer.writerow(row)

# Parameters
input_file = "AAPL_historical_data.csv"  # Path to your uploaded file
output_file = "AAPL_preprocessed_data.csv"  # Path to save processed file

# Process data
try:
    preprocessed_data = preprocess_financial_data(input_file)

    # Save preprocessed data
    save_preprocessed_data(preprocessed_data, output_file)

    print(f"Preprocessed data saved to {output_file}")
except Exception as e:
    print(f"An error occurred: {e}")
