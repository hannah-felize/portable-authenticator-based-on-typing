import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json
import pickle

def preprocess_data(df):
    # Preprocess Data
    # Extract the typing data from the 'typing_data' column
    typing_data_df = df['typing_data'].apply(json.loads)

    # Get the maximum number of key presses of all typing tests
    # max_key_presses = 0
    # count_key_presses = 0
    # for typing_test in typing_data_df:
    #     for key_press in typing_test:
    #         count_key_presses += 1
    #         if count_key_presses > max_key_presses:
    #             max_key_presses = count_key_presses
    #     count_key_presses = 0

    max_key_presses = 75

    # Create a new DataFrame to store the preprocessed typing data
    preprocessed_data = {'user': []}
    for i in range(1, max_key_presses+1):
        preprocessed_data[f'key_pressed_{i}'] = []
        preprocessed_data[f'previous_key_pressed_{i}'] = []
        preprocessed_data[f'time_between_presses_{i}'] = []

    # Preprocess the typing data
    for index, row in df.iterrows():
        user = row['user']
        typing_data = json.loads(row['typing_data'])
        preprocessed_data['user'].append(user)
        for i in range(max_key_presses):
            if i < len(typing_data):
                key_press = typing_data[i]
                preprocessed_data[f'key_pressed_{i+1}'].append(key_press['key_pressed'])
                preprocessed_data[f'previous_key_pressed_{i+1}'].append(key_press['previous_key_pressed'])
                preprocessed_data[f'time_between_presses_{i+1}'].append(key_press['time_between_presses'])
            else:
                preprocessed_data[f'key_pressed_{i+1}'].append(None)
                preprocessed_data[f'previous_key_pressed_{i+1}'].append(None)
                preprocessed_data[f'time_between_presses_{i+1}'].append(None)

    # Create a new DataFrame from the preprocessed data
    preprocessed_df = pd.DataFrame(preprocessed_data)

    # Create a LabelEncoder
    le = LabelEncoder()

    # Fit the LabelEncoder on the 'key_pressed' and 'previous_key_pressed' columns
    for i in range(1, max_key_presses+1):
        preprocessed_df[f'key_pressed_{i}'] = le.fit_transform(preprocessed_df[f'key_pressed_{i}'])
        preprocessed_df[f'previous_key_pressed_{i}'] = le.fit_transform(preprocessed_df[f'previous_key_pressed_{i}'])

    # Fill NaN values in the feature columns with 0
    feature_columns = [col for col in preprocessed_df.columns if col != 'user']
    preprocessed_df[feature_columns] = preprocessed_df[feature_columns].fillna(0)

    # Features are all columns except 'user'
    X = preprocessed_df.drop('user', axis=1)

    # Target is the 'user' column
    y = preprocessed_df['user']

    return X, y

def train_model(X_train, y_train):
    # Choose Model
    model = RandomForestClassifier()

    # Train Model
    model.fit(X_train, y_train)

    # Save the trained model to a file
    with open('trained_model.pkl', 'wb') as file:
        pickle.dump(model, file)

def evaluate_model(model, X_test, y_test):
    # Evaluate Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

def make_predictions(model, X):
    # Make Predictions
    predictions = model.predict(X)
    return predictions

def main():
    # Connect to the database
    conn = sqlite3.connect('typing_tests.db')

    # Read data from the database into a DataFrame
    query = "SELECT * FROM typing_data"
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Preprocess the data
    X, y = preprocess_data(df)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    train_model(X_train, y_train)

    # Load the trained model from the file
    with open('trained_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Make predictions
    predictions = make_predictions(model, X)

if __name__ == "__main__":
    main()