import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv('2020_bn_nb_data.csv')

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Apply LabelEncoder to each categorical column (except for the target column)
data['EC100'] = label_encoder.fit_transform(data['EC100'])
data['IT101'] = label_encoder.fit_transform(data['IT101'])
data['MA101'] = label_encoder.fit_transform(data['MA101'])
data['PH100'] = label_encoder.fit_transform(data['PH100'])
data['Internship_Qualification'] = label_encoder.fit_transform(data['Internship_Qualification'])

# Initialize Naive Bayes Classifier for independent variables
naive_bayes_classifier = CategoricalNB()

# Repeat the experiment 20 times
accuracies = []
for i in range(20):
    # Split data into training and testing sets (70% training, 30% testing)
    train_data, test_data = train_test_split(data, test_size=0.3)
    
    # Separate features and labels
    X_train = train_data.drop('Internship_Qualification', axis=1)
    y_train = train_data['Internship_Qualification']
    X_test = test_data.drop('Internship_Qualification', axis=1)
    y_test = test_data['Internship_Qualification']
    
    # Initialize LabelEncoder for each feature column
    le_dict = {}
    
    # Fit LabelEncoder on the entire dataset for each feature
    for col in X_train.columns:
        le = LabelEncoder()
        le.fit(data[col])  # Fit the encoder on the entire dataset (train + test)
        le_dict[col] = le
        
        # Transform both train and test data using the fitted encoder
        X_train[col] = le.transform(X_train[col])
        X_test[col] = le.transform(X_test[col])
    
    # Train the classifier
    naive_bayes_classifier.fit(X_train, y_train)
    
    # Predict and calculate accuracy
    y_pred = naive_bayes_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

# Report accuracy results
mean_accuracy = sum(accuracies) / len(accuracies)
print(f"Mean accuracy: {mean_accuracy:.2f}")
