import sqlite3
import time
import msvcrt

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

    typing_data = []  # Array to store typing test data

    while True:
        key = msvcrt.getche()

        if key == b'\r':  # Enter key
            break

        current_time = time.time()
        time_between_presses = current_time - start_time

        # Save the typing test data to the array
        typing_data.append((user, key, previous_key, time_between_presses))

        previous_key = key
        start_time = current_time

    # Insert the typing test data into the database
    cursor.executemany('''
        INSERT INTO typing_data (user, key_pressed, previous_key_pressed, time_between_presses)
        VALUES (?, ?, ?, ?)
    ''', typing_data)
    conn.commit()
    print("Typing test completed. Thank you!")

# Usage example
conduct_typing_test("John Doe")

# Close the database connection
conn.close()