import sqlite3
import time

# Connect to the database
conn = sqlite3.connect('typing_test.db')
cursor = conn.cursor()

# Create a table to store typing test data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS typing_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        key_pressed TEXT,
        previous_key_pressed TEXT,
        time_between_presses REAL
    )
''')

def conduct_typing_test(user):
    print("Welcome to the typing test!")
    print("Type the given text and press Enter when you're done.")

    text = "This is a sample typing test."  # Replace with your own text

    start_time = time.time()
    previous_key = None

    while True:
        key = input()

        if key == "":
            break

        current_time = time.time()
        time_between_presses = current_time - start_time

        # Save the typing test data to the database
        cursor.execute('''
            INSERT INTO typing_data (user, key_pressed, previous_key_pressed, time_between_presses)
            VALUES (?, ?, ?, ?)
        ''', (user, key, previous_key, time_between_presses))
        conn.commit()

        previous_key = key
        start_time = current_time

    print("Typing test completed. Thank you!")

# Usage example
conduct_typing_test("John Doe")

# Close the database connection
conn.close()