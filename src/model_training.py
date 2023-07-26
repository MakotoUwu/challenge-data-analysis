import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

os.makedirs('../models', exist_ok=True)

def train_and_test_model(model, X_train, X_test, y_train, y_test, property_type, region):
    """
    Trains a model on the provided training data and tests it on the test data. 

    This function fits the model on the training data, makes predictions on both training and test sets, 
    then calculates and prints the mean squared error (MSE) and coefficient of determination (R^2 score) 
    for both the training and test sets.

    Parameters:
    model (sklearn.base.BaseEstimator): The machine learning model to be trained.
    X_train (numpy.ndarray): The training feature set.
    X_test (numpy.ndarray): The test feature set.
    y_train (numpy.ndarray): The training target set.
    y_test (numpy.ndarray): The test target set.
    property_type (str): The type of property, used for printing results.
    region (str): The region of the property, used for printing results.

    Returns:
    None
    """

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Save the trained model to disk
    filename = f'../models/{property_type}_{region}_model.pickle'
    pickle.dump(model, open(filename, 'wb'))

    # Make predictions on the training set and the test set
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Calculate the mean squared error for the training set and print it
    print(f'Mean squared error (train) for {property_type} in {region}: %.2f'
          % mean_squared_error(y_train, y_train_pred))

    # Calculate the mean squared error for the test set and print it
    print(f'Mean squared error (test) for {property_type} in {region}: %.2f'
          % mean_squared_error(y_test, y_test_pred))

    # Calculate the coefficient of determination (R^2) for the training set and print it
    print(f'Coefficient of determination R^2 (train) for {property_type} in {region}: %.2f'
          % r2_score(y_train, y_train_pred))

    # Calculate the coefficient of determination (R^2) for the test set and print it
    print(f'Coefficient of determination R^2 (test) for {property_type} in {region}: %.2f'
          % r2_score(y_test, y_test_pred))

    
def train_models(X_train, X_test, y_train, y_test, property_type, region):
    """
    Trains both a Linear Regression and an XGBoost Regression model on the provided training data 
    and tests it on the test data.

    This function creates instances of LinearRegression and XGBRegressor models, then trains and tests 
    each model using the 'train_and_test_model' function, providing performance metrics for each model.

    Parameters:
    X_train (numpy.ndarray): The training feature set.
    X_test (numpy.ndarray): The test feature set.
    y_train (numpy.ndarray): The training target set.
    y_test (numpy.ndarray): The test target set.
    property_type (str): The type of property, used for printing results.
    region (str): The region of the property, used for printing results.

    Returns:
    None
    """

    # Train and test Linear Regression model
    print(f"----Linear Regression Results for {property_type} in {region}----")
    lr_model = LinearRegression()  # Create an instance of Linear Regression
    train_and_test_model(lr_model, X_train, X_test, y_train, y_test, property_type, region)

    # Train and test XGBoost Regression model
    print(f"----XGBoost Regression Results for {property_type} in {region}----")
    xgb_model = XGBRegressor(objective ='reg:squarederror')  # Create an instance of XGBoost Regression and set the objective to 'reg:squarederror' to suppress a warning from XGBoost
    train_and_test_model(xgb_model, X_train, X_test, y_train, y_test, property_type, region)

def split_data(X, y):
    """
    Splits the data into training and test sets, and scales the features.

    This function uses sklearn's train_test_split function to split the input data 
    into training and test sets. The split is stratified, and the test set size is 20% 
    of the total dataset. It uses a fixed random state (42) for reproducibility.

    The function then scales the features using sklearn's StandardScaler.

    Parameters:
    X (pandas.DataFrame): The input features.
    y (pandas.Series): The target variable.

    Returns:
    numpy.ndarray: The training feature set, test feature set, training target set, and test target set.
    """

    # Split the data into training and test sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize a standard scaler
    scaler = StandardScaler()

    # Fit the scaler on the training data and transform the training data
    X_train = scaler.fit_transform(X_train)

    # Transform the test data using the fitted scaler
    X_test = scaler.transform(X_test)

    # Return the training and test sets
    return X_train, X_test, y_train, y_test
