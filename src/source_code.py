import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import seaborn as sns

# Define the function to get the region from the zip code
def get_region(zip_code):
    if 1000 <= zip_code <= 1299:
        return 'Brussels-Capital'
    elif 1300 <= zip_code <= 1499:
        return 'Walloon Brabant'
    elif (1500 <= zip_code <= 1999) or (3000 <= zip_code <= 3499):
        return 'Flemish Brabant'
    elif 2000 <= zip_code <= 2999:
        return 'Antwerp'
    elif 3500 <= zip_code <= 3999:
        return 'Limburg'
    elif 4000 <= zip_code <= 4999:
        return 'Liege'
    elif 5000 <= zip_code <= 5999:
        return 'Namur'
    elif (6000 <= zip_code <= 6599) or (7000 <= zip_code <= 7999):
        return 'Hainaut'
    elif 6600 <= zip_code <= 6999:
        return 'Luxembourg'
    elif 8000 <= zip_code <= 8999:
        return 'West Flanders'
    elif 9000 <= zip_code <= 9999:
        return 'East Flanders'

def load_and_clean_data(path):
    # Load the DataFrame
    df = pd.read_csv('../data/property_data.csv')

    # Drop duplicates
    df = df.drop_duplicates()

    # Add a 'Region' column
    df['Region'] = df['Zip code'].apply(get_region)

    # Drop unnecessary columns
    columns_to_drop = ['Zip code', 'Locality','Type of Sale','State of the building', 'Subtype of property','Garden', 'Swimming pool', 'Terrace', 'Kitchen', 'Raw num:', 'ID number', 'URL']
    df = df.drop(columns=columns_to_drop)

    return df

def drop_highly_correlated_features(df):
    numeric_df = df.select_dtypes(include=[np.number])# Select only numeric columns for correlation
    correlation_matrix = numeric_df.corr().abs()
    upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool_))
    to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > 0.95)]
    df = df.drop(df[to_drop], axis=1)
    return df

def preprocess_group_df(group_df, property_type):
    group_df = drop_highly_correlated_features(group_df)
    
    if property_type == 'apartment':
        if 'Garden area' in group_df.columns:
            group_df = group_df.drop(columns=['Garden area'])

    group_df = group_df.fillna(0)
    
    return group_df

def split_data(X, y):
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def train_and_test_model(model, X_train, X_test, y_train, y_test, property_type, region):
    model.fit(X_train, y_train)

    # Make predictions using the testing set
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # The mean squared error
    print(f'Mean squared error (train) for {property_type} in {region}: %.2f'
          % mean_squared_error(y_train, y_train_pred))

    print(f'Mean squared error (test) for {property_type} in {region}: %.2f'
          % mean_squared_error(y_test, y_test_pred))

    # The coefficient of determination: 1 is perfect prediction
    print(f'Coefficient of determination R^2 (train) for {property_type} in {region}: %.2f'
          % r2_score(y_train, y_train_pred))

    print(f'Coefficient of determination R^2 (test) for {property_type} in {region}: %.2f'
          % r2_score(y_test, y_test_pred))

def train_models(X_train, X_test, y_train, y_test, property_type, region):
    print(f"----Linear Regression Results for {property_type} in {region}----")
    lr_model = LinearRegression()
    train_and_test_model(lr_model, X_train, X_test, y_train, y_test, property_type, region)

    print(f"----XGBoost Regression Results for {property_type} in {region}----")
    xgb_model = XGBRegressor(objective ='reg:squarederror') # To silent the warning from XGBoost
    train_and_test_model(xgb_model, X_train, X_test, y_train, y_test, property_type, region)


def plot_actual_vs_predicted(X, y, property_type, region):
    if 'Living area' not in X.columns:
        return

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    # Make predictions using the whole dataset
    y_pred = model.predict(X_scaled)

    # Plot outputs
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X['Living area'], y=y, label='Actual Price')
    sns.lineplot(x=X['Living area'], y=y_pred, color='red', label='Predicted Price')
    plt.xlabel('Living Area')
    plt.ylabel('Price of property in euro')
    plt.title(f'Price vs Living Area for {property_type} in {region}')
    plt.legend()
    plt.show()

def get_property_restrictions():
    return {
        ('apartment', 'East Flanders'): {'Living area': 300, 'Price of property in euro': 600000},
        ('apartment', 'Hainaut'): {'Living area': 175, 'Price of property in euro': 350000},
        ('apartment', 'West Flanders'): {'Living area': 150, 'Price of property in euro': 600000},
        ('apartment', 'Flemish Brabant'): {'Living area': 300, 'Price of property in euro': 800000},
        ('apartment', 'Liege'): {'Living area': 300, 'Price of property in euro': 600000},
        ('apartment', 'Limburg'): {'Living area': 170, 'Price of property in euro': 640000},
        ('apartment', 'Luxembourg'): {'Living area': 150, 'Price of property in euro': 450000},
        ('apartment', 'Namur'): {'Living area': 140, 'Price of property in euro': 600000},
        ('house', 'Antwerp'): {'Living area': 800, 'Price of property in euro': 3000000},
        ('house', 'East Flanders'): {'Living area': 800, 'Price of property in euro': 1500000},
        ('house', 'Flemish Brabant'): {'Living area': 800, 'Price of property in euro': 4000000},
        ('house', 'Hainaut'): {'Living area': 600, 'Price of property in euro': 1000000},
        ('house', 'Liege'): {'Living area': 800, 'Price of property in euro': 1500000},
        ('house', 'Luxembourg'): {'Living area': 350, 'Price of property in euro': 800000},
        ('house', 'Namur'): {'Living area': 800, 'Price of property in euro': 700000},
        ('house', 'Walloon Brabant'): {'Living area': 800, 'Price of property in euro': 2500000},
        ('house', 'West Flanders'): {'Living area': 500, 'Price of property in euro': 1000000}
    }


def filter_data(group_df, property_type, region): #to get rig off otliners
    property_restrictions = get_property_restrictions()
    if (property_type, region) in property_restrictions:
        restrictions = property_restrictions[(property_type, region)]
        group_df = group_df[(group_df['Living area'] <= restrictions['Living area']) &
                            (group_df['Price of property in euro'] <= restrictions['Price of property in euro'])]
    return group_df

# ... and so on for the rest of your functions
