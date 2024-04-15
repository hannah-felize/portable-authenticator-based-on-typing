import sqlite3
import time
import curses
import random
import json

# Define multiple variations of typing test text
typing_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How razorback-jumping frogs can level six piqued gymnasts!",
    "Crazy Fredrick bought many very exquisite opal jewels.",
    "Sixty zippers were quickly picked from the woven jute bag.",
    "A quick movement of the enemy will jeopardize six gunboats.",
    "All questions asked by five watch experts amazed the judge.",
    "Jack quietly moved up front and seized the big ball of wax.",
    "The job requires extra pluck and zeal from every young wage earner.",
    "The exodus of jazzy pigeons is craved by squeamish walkers.",
    "The juke box music puzzled a gentle visitor from a quaint valley.",
    "Six big devils from Japan quickly forgot how to waltz.",
    "Big July earthquakes confound zany experimental vow."
]

def conduct_typing_test():
    stdscr = curses.initscr()
    stdscr.clear()

    try:
        stdscr.addstr("Welcome to the typing test!\n")
        stdscr.addstr("Please enter your name: ")
        stdscr.refresh()

        user = stdscr.getstr()
        if isinstance(user, bytes):
            user = user.decode('utf-8')

        stdscr.addstr("Type the given text and press Enter when you're done.\n")
        stdscr.refresh()

        text = random.choice(typing_texts)  # Replace with your own text

        stdscr.addstr(text + "\n")
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
            typing_data.append({"key_pressed": chr(key), "previous_key_pressed": chr(previous_key) if previous_key else None, "time_between_presses": time_between_presses})

            previous_key = key
            start_time = current_time

        # Return the typing data and user name
        return user, typing_data

    finally:
        curses.endwin()

def main():
    # Connect to the database
    conn = sqlite3.connect('typing_test.db')
    cursor = conn.cursor()

    # Create a table to store typing test data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS typing_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            typing_data TEXT
        )
    ''')

    # Conduct typing test
    user, typing_data = conduct_typing_test()

    # Convert typing data to JSON format
    typing_data_json = json.dumps(typing_data)

    # Insert the typing test data into the database
    cursor.execute('''
        INSERT INTO typing_data (user, typing_data)
        VALUES (?, ?)
    ''', (user, typing_data_json))
    conn.commit()

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()