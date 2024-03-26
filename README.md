# Portable Authenticator Based on Typing

This Python program is designed to run on a Raspberry Pi and provides a typing test authentication system. It takes a typing test as input and outputs a percent confidence level predicting the user who typed it. If the confidence level is above a certain threshold, the user is deemed "authenticated".

## Features

- User performs a set of typing tests, and the data is stored in a database.
- The typing test data is used as the training set for a selected machine learning algorithm.
- Data features include the key pressed, previous key pressed, and time between key presses.
- The target variable is the username of the user.
- The database contains training data from multiple users.

## Usage

1. Install the required dependencies by running the following command:

   ```bash
   $ pip install -r requirements.txt
   ```

2. Run the program by executing the following command:

   ```bash
   $ python typing_authenticator.py
   ```

3. Follow the on-screen instructions to perform the typing test.

4. The program will output a confidence level identifying which user it predicts to have done the typing.
