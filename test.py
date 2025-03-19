import joblib
import pandas as pd

# Load the saved model
model = joblib.load("water_scarcity_model.pkl")

# Define function for prediction
def predict_scarcity(input_data):
    """
    Predicts water scarcity level based on input rainfall data.
    :param input_data: Dictionary with monthly and seasonal rainfall values.
    :return: Predicted scarcity level.
    """
    # Convert input data to DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Ensure column order matches training data
    expected_features = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'Jan-Feb', 'Mar-May', 'Jun-Sep', 'ANNUAL']
    df_input = df_input.reindex(columns=expected_features, fill_value=0)
    
    # Predict
    prediction = model.predict(df_input)[0]
    
    # Decode the prediction
    scarcity_levels = ["Moderate Scarcity", "No Scarcity", "Severe Scarcity"]
    return scarcity_levels[prediction]

# Example usage
if __name__ == "__main__":

    # IF Quick Predict:
    d = {
        "JAN":0,"FEB":0,"MAR": 0, "APR": 0, "MAY": 0, "JUN": 0,
        "JUL": 0, "AUG": 0, "SEP": 0, "OCT": 0, "NOV": 0, "DEC": 0,
        "Jan-Feb": 0, "Mar-May": 0, "Jun-Sep": 0, "ANNUAL":0
        }
    a1 = input("Enter annual rainfall of previous year (mm): ")
    a2 = a1/12
    for i in d:
        if i == "Jan-Feb":
            d[i] = a2*2
        elif i == "Mar-May":
            d[i] = a2*3
        elif i == "Jun-Sep":
            d[i] = a2*4
        elif i != "ANNUAL":
            d[i] = a2
        

    # ELSE IF DETAILED PREDICT:
    
    sample_input = {
        "JAN": 20, "FEB": 30, "MAR": 50, "APR": 70, "MAY": 100, "JUN": 200,
        "JUL": 300, "AUG": 250, "SEP": 180, "OCT": 90, "NOV": 60, "DEC": 40,
        "Jan-Feb": 50, "Mar-May": 220, "Jun-Sep": 930, "ANNUAL": 1200
    }
    
    result = predict_scarcity(sample_input)
    print("Predicted Water Scarcity Level:", result)

