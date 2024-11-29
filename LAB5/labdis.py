import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Load the dataset
data = pd.read_csv('2020_bn_nb_data.csv')

# Inspect the dataset
print(data.info())
for col in data.columns:
    print(f"{col}: {data[col].unique()}")

# Encode categorical features
encoder = LabelEncoder()
for col in data.columns:
    if data[col].dtype == 'object':
        data[col] = encoder.fit_transform(data[col])

# Split the data into features and target
X = data.drop('Internship_Qualification', axis=1)
y = data['Internship_Qualification']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize Naive Bayes Classifier
naive_bayes_classifier = CategoricalNB()

# Train the classifier
naive_bayes_classifier.fit(X_train, y_train)

# Predict and calculate accuracy
y_pred = naive_bayes_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")