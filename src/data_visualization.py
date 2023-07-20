import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

def plot_actual_vs_predicted(X, y, property_type, region):
    """
    Plots a scatter plot of the actual property prices versus the predicted property prices based on living area.

    The function fits a Linear Regression model on the entire dataset, then makes predictions and plots 
    the actual prices against the predicted prices. This plot is useful for visually inspecting the 
    model's performance. The function only plots if the 'Living area' feature is present in the dataset.

    Parameters:
    X (pandas.DataFrame): The feature set, should include 'Living area' for plot.
    y (pandas.Series or numpy.ndarray): The target set.
    property_type (str): The type of property, used for plot title.
    region (str): The region of the property, used for plot title.

    Returns:
    None
    """
    
    # Check if 'Living area' is present in the dataset
    if 'Living area' not in X.columns:
        return

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create and fit the Linear Regression model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Make predictions using the entire dataset
    y_pred = model.predict(X_scaled)

    # Plot actual prices vs predicted prices
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X['Living area'], y=y, label='Actual Price')  # Scatter plot of actual prices
    sns.lineplot(x=X['Living area'], y=y_pred, color='red', label='Predicted Price')  # Line plot of predicted prices
    plt.xlabel('Living Area')
    plt.ylabel('Price of property in euro')
    plt.title(f'Price vs Living Area for {property_type} in {region}')  # Set the title of the plot
    plt.legend()
    plt.show()