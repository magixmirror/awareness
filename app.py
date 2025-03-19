import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load the saved model
model = joblib.load("water_scarcity_model.pkl")

def predict_scarcity(input_data):
    """
    Predicts water scarcity level based on input rainfall data.
    :param input_data: Dictionary with monthly and seasonal rainfall values.
    :return: Predicted scarcity level.
    """
    # Convert input data to DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Get feature names from the model (requires scikit-learn >= 1.0)
    expected_features = model.feature_names_in_
    
    # Ensure column order matches training data
    df_input = df_input.reindex(columns=expected_features, fill_value=0)
    
    # Predict
    prediction = model.predict(df_input)[0]
    
    # Decode the prediction
    scarcity_levels = ["Moderate Scarcity", "No Scarcity", "Severe Scarcity"]
    return scarcity_levels[prediction]

# Set page configuration
st.set_page_config(page_title="Wave Of Awareness - Solving Water Scarcity", layout="wide")

# Landing Page
st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center; height: 100vh;'>
        <h1 style='text-align: center; font-size: 80px; font-weight: bold; color: white;'>
        Wave Of Awareness<br>Solving Water Scarcity
        </h1>
    </div>
""", unsafe_allow_html=True)

# Overview
st.markdown("---")
st.markdown("## Overview")
st.markdown(
    """
    * Water scarcity is a pressing global issue that impacts millions of people daily. It occurs when the demand for freshwater exceeds its availability due to factors such as climate change, population growth, pollution, and inefficient water management. As freshwater resources continue to decline, common people face severe consequences in their daily lives.

    * One of the most immediate effects of water scarcity is the lack of access to clean drinking water. Millions of people, especially in developing countries, are forced to rely on unsafe water sources, leading to the spread of diseases such as cholera, dysentery, and typhoid. Additionally, inadequate water supply affects sanitation, increasing the risk of infections and poor hygiene practices.

    * Water scarcity also has a significant economic impact. Farmers, particularly in drought-prone regions, struggle with crop failure due to insufficient irrigation. This leads to reduced food production, rising food prices, and economic instability. Urban areas are not immune either—industries that depend on water, such as manufacturing and energy production, face operational challenges, leading to job losses and financial hardships.

    * Women and children are disproportionately affected, as they often bear the burden of collecting water from distant sources, reducing their time for education and work. In many regions, water scarcity leads to conflicts among communities and even between nations, as competition for water resources intensifies.

    * Addressing water scarcity requires sustainable solutions, including water conservation, efficient management, rainwater harvesting, and the promotion of renewable energy sources. Only through collective action can we ensure water security for future generations.
    """
)

# Prediction Section
st.markdown("---")
st.markdown("## Will Bangalore Run Dry? Predicting the Future")
option = st.radio("\nSelect Prediction Mode:", ["Quick Predict", "Detailed Prediction"], horizontal=True)

if option == "Quick Predict":
    annual_rainfall = st.number_input("Enter Annual Rainfall (mm):", min_value=0, max_value=5000, step=10)
    if st.button("Predict"):
        avg_monthly = annual_rainfall / 12
        input_data = {month: avg_monthly for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']}
        input_data["Jan-Feb"] = avg_monthly * 2
        input_data["Mar-May"] = avg_monthly * 3
        input_data["Jun-Sep"] = avg_monthly * 4
        input_data["ANNUAL"] = annual_rainfall
        result = predict_scarcity(input_data)
        st.write(f"### Prediction: {result}")

elif option == "Detailed Prediction":
    monthly_rainfall = {}
    for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
        monthly_rainfall[month] = st.number_input(f"{month} Rainfall (mm):", min_value=0, max_value=500, step=5)
    
    if st.button("Predict"):
        monthly_rainfall["Jan-Feb"] = monthly_rainfall["JAN"] + monthly_rainfall["FEB"]
        monthly_rainfall["Mar-May"] = monthly_rainfall["MAR"] + monthly_rainfall["APR"] + monthly_rainfall["MAY"]
        monthly_rainfall["Jun-Sep"] = monthly_rainfall["JUN"] + monthly_rainfall["JUL"] + monthly_rainfall["AUG"] + monthly_rainfall["SEP"]
        monthly_rainfall["ANNUAL"] = sum(monthly_rainfall.values())
        result = predict_scarcity(monthly_rainfall)
        st.write(f"### Prediction: {result}")


# Results Section
st.markdown("---")
st.markdown("## Results")

# Import dataset
rainfall_data = pd.read_csv("rainfall_area-wt_India_1901-2015.csv")

# Filter data from year 2000 onwards
recent_data = rainfall_data[rainfall_data['YEAR'] >= 2000]

# Create a compact figure
fig, ax = plt.subplots(figsize=(4, 2.5))  # Reduced figure size
plt.tight_layout()

# Plot styling for small size
ax.plot(recent_data['YEAR'], recent_data['ANNUAL'], 
        marker='o', markersize=4, linewidth=1.5, 
        color='#1f77b4', linestyle='-')
ax.set_xlabel("Year", fontsize=9, labelpad=5)
ax.set_ylabel("Rainfall (mm)", fontsize=9, labelpad=5)
ax.set_title("Annual Rainfall (2000-2015)", fontsize=10, pad=10)
ax.grid(True, linewidth=0.5)
ax.tick_params(axis='both', which='major', labelsize=8)
ax.set_xticks(recent_data['YEAR'])
ax.tick_params(axis='x', rotation=45, pad=2)

# Adjust spacing
plt.subplots_adjust(bottom=0.25, left=0.18, right=0.95, top=0.85)

# Centered container with compact styling
st.markdown("""
    <div style="
        display: flex;
        justify-content: center;
        padding: 20px 10px 10px 10px;
        margin: 15px auto;
        max-width: 65%;
    ">
""", unsafe_allow_html=True)

st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    - Shows rainfall trends from 2000-2015
    - Highlights recent water availability patterns
    - Focused on contemporary climate data
    
""")

# Conservation Section
st.markdown("---")
st.markdown("## What You Can Do: Simple Steps for Conservation")
st.markdown(
    """
    At BangaloreWaterCrisis.com, we are dedicated to spreading awareness about the pressing water scarcity issues in Bangalore. Our platform offers valuable insights, updates, and resources to empower individuals to take action and make a difference.
    Our goal is to provide a comprehensive understanding of the water crisis in Bangalore through informative articles, educational content, and interactive tools. By raising awareness, we strive to inspire positive change and sustainable solutions for a better future.
    - Use Water-Efficient Appliances
    - Opt for low-flow taps and water-saving devices.
    - Limit Water Use
    - Shorten showers and turn off taps while brushing.
    - Reuse Water
    - Use treated greywater for gardening and cleaning.
    - Sustainable Landscaping
    - Grow drought-resistant plants to reduce water consumption.
    - Community Awareness
    - Educate others on water conservation practices.
    """
)

# Ending Tile
st.write("---")
st.caption("""
           © 2025 Water Scarcity Awarness Initative\n
           Team:\tDeva\tElsa\tArdra\tLakshmi\tPallavi\tDais            
""")