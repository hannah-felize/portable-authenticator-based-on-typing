import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json

# Connect to the database
conn = sqlite3.connect('typing_test.db')

# Preprocess Data
# Read data from the database into a DataFrame
query = "SELECT * FROM typing_data"
df = pd.read_sql_query(query, conn)

# Extract the typing data from the 'typing_data' column
typing_data_df = df['typing_data'].apply(json.loads)

# Get the maximum number of key presses of all typing tests
max_key_presses = 0
count_key_presses = 0
for typing_test in typing_data_df:
    for key_press in typing_test:
        count_key_presses += 1
        if count_key_presses > max_key_presses:
            max_key_presses = count_key_presses
    count_key_presses = 0
print(max_key_presses)

# Create a new sqlite3 table to store the preprocessed typing data
cursor = conn.cursor()
table_columns = ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'user TEXT']
for i in range(1, max_key_presses+1):
    table_columns.append(f'key_pressed_{i} TEXT')
    table_columns.append(f'previous_key_pressed_{i} TEXT')
    table_columns.append(f'time_between_presses_{i} REAL')

table_columns_str = ', '.join(table_columns)

cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS preprocessed_typing_data (
        {table_columns_str}
    )
''')

# Copy all data from the 'typing_data' table to the 'preprocessed_typing_data' table
for index, row in df.iterrows():
    user = row['user']
    typing_data = json.loads(row['typing_data'])
    typing_data_dict = {'user': user}
    for i, key_press in enumerate(typing_data):
        typing_data_dict[f'key_pressed_{i+1}'] = key_press['key_pressed']
        typing_data_dict[f'previous_key_pressed_{i+1}'] = key_press['previous_key_pressed']
        typing_data_dict[f'time_between_presses_{i+1}'] = key_press['time_between_presses']

    # Insert the preprocessed typing data into the new table
    columns = ', '.join(typing_data_dict.keys())
    placeholders = ', '.join(['?' for _ in typing_data_dict.values()])
    values = list(typing_data_dict.values())

    cursor.execute(f'''
        INSERT INTO preprocessed_typing_data ({columns})
        VALUES ({placeholders})
    ''', values)
    conn.commit()

# # Features are all columns except 'user'
# X = df.drop('user', axis=1)

# # Target is the 'user' column
# y = df['user']

# # Split data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Choose Model
# model = RandomForestClassifier()

# # Train Model
# model.fit(X_train, y_train)

# # Evaluate Model
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)

# # Make Predictions
# # You can now use the trained model to make predictions on new typing test data
# # For example, you can use X_test or new data
# predictions = model.predict(X_test)

# Close the database connection
conn.close()
