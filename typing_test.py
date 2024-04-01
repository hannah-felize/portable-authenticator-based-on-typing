import sqlite3
import time
import curses

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
    stdscr = curses.initscr()
    curses.noecho()  # Disable automatic echoing of key presses
    stdscr.clear()

    stdscr.addstr("Welcome to the typing test!\n")
    stdscr.addstr("Type the given text and press Enter when you're done.\n")
    stdscr.refresh()

    text = "This is a sample typing test."  # Replace with your own text

    start_time = time.time()
    previous_key = None

    typing_data = []  # Array to store typing test data

    while True:
        key = stdscr.getch()

        if key == ord('\n'):  # Enter key
            break

        current_time = time.time()
        time_between_presses = current_time - start_time

        # Save the typing test data to the array
        typing_data.append((user, chr(key), chr(previous_key) if previous_key else None, time_between_presses))

        previous_key = key
        start_time = current_time

    # Insert the typing test data into the database
    cursor.executemany('''
        INSERT INTO typing_data (user, key_pressed, previous_key_pressed, time_between_presses)
        VALUES (?, ?, ?, ?)
    ''', typing_data)
    conn.commit()
    stdscr.addstr("Typing test completed. Thank you!\n")
    stdscr.refresh()
    curses.echo()  # Re-enable echoing of key presses
    stdscr.getch()  # Wait for a key press before exiting

# Usage example
conduct_typing_test("John Doe")

# Close the database connection
conn.close()
