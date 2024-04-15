import pickle
from typing_trainer import conduct_typing_test
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
    print("===== The predicted user is:", prediction[0], "=====")
    # Get the top 3 predictions and confidence levels
    top_predictions = model.predict_proba(X)[0].argsort()[-3:][::-1]
    confidence_levels = model.predict_proba(X)[0][top_predictions]

    # Print the top 3 predictions and confidence levels
    for prediction, confidence in zip(top_predictions, confidence_levels):
        print("Prediction: User", prediction)
        print("Confidence Level:", confidence)

if __name__ == "__main__":
    main()