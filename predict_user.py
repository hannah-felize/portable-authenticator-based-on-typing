import pickle
from typing_test import conduct_typing_test
from rf_classifier import preprocess_data
import pandas as pd
import json

def main():
    # Prompt the user to do a typing test
    user, typing_data = conduct_typing_test()

    # Convert the typing data to a DataFrame
    df = pd.DataFrame({'id': 1, 'user': user, 'typing_data': [json.dumps(typing_data)]})

    # # Perform preprocessing
    X, y = preprocess_data(df)

    # # Load the trained model
    with open('trained_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Make a prediction
    prediction = model.predict(X)

    # Print the prediction
    print("The predicted user is:", prediction[0])

if __name__ == "__main__":
    main()