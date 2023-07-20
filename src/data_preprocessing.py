import pandas as pd
import numpy as np


def get_region(zip_code):
    """
    Get the region name based on the given zip code.

    This function takes a zip code as input and returns the corresponding region in Belgium. 
    It uses specific ranges of zip codes for different regions as defined by the Belgium postal system.

    Parameters:
    zip_code (int): The zip code as an integer.

    Returns:
    str: The region corresponding to the given zip code. If the zip code is not in a defined range, it returns None.

    """
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
    """
    Load the dataset from a csv file and perform initial cleaning operations.

    This function takes the path of a csv file as input, loads it into a pandas DataFrame, 
    and performs several cleaning operations such as dropping duplicates, adding a new column for 'Region' 
    (derived from 'Zip code' using the get_region function), and removing unnecessary columns.

    Parameters:
    path (str): The file path to the csv data.

    Returns:
    pandas.DataFrame: A cleaned DataFrame ready for further preprocessing and analysis.

    """
    # Load the DataFrame from the given csv file path
    df = pd.read_csv(path)

    # Drop duplicate rows from the DataFrame
    df = df.drop_duplicates()

    # Add a 'Region' column to the DataFrame
    # The 'Region' values are determined by applying the get_region function to the 'Zip code' column
    df['Region'] = df['Zip code'].apply(get_region)

    # Define a list of columns that are unnecessary for the analysis
    columns_to_drop = ['Zip code', 'Locality', 'Type of Sale', 'State of the building', 
                       'Subtype of property', 'Garden', 'Swimming pool', 'Terrace', 
                       'Kitchen', 'Raw num:', 'ID number', 'URL']

    # Drop the unnecessary columns from the DataFrame
    df = df.drop(columns=columns_to_drop)

    # Return the cleaned DataFrame
    return df

def drop_highly_correlated_features(df):
    """
    Remove features from a DataFrame that are highly correlated with other features.

    This function computes the pairwise correlation of all columns in the DataFrame, and if any 
    two features have a correlation higher than 0.95, it drops one of them. 

    Parameters:
    df (pandas.DataFrame): The input DataFrame.

    Returns:
    pandas.DataFrame: A DataFrame with highly correlated features removed.

    """
    # Create a new DataFrame containing only numeric columns from the input DataFrame
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Compute the correlation matrix of the numeric columns
    correlation_matrix = numeric_df.corr().abs()

    # Compute a mask for the upper triangle of the correlation matrix
    upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool_))

    # Identify columns whose correlation with any other column is greater than 0.95
    to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > 0.95)]

    # Drop these columns from the input DataFrame
    df = df.drop(df[to_drop], axis=1)

    # Return the resulting DataFrame
    return df

def preprocess_group_df(group_df, property_type):
    """
    Preprocesses the input DataFrame specific to the property type.

    This function first drops the highly correlated features from the input DataFrame.
    If the property type is 'apartment', it also removes the 'Garden area' column, if present.
    Then, it fills any remaining NaN values in the DataFrame with 0.

    Parameters:
    group_df (pandas.DataFrame): The input DataFrame to be preprocessed.
    property_type (str): The type of property (e.g., 'apartment', 'house', etc.).

    Returns:
    pandas.DataFrame: The preprocessed DataFrame.
    """

    # Drop highly correlated features from the DataFrame
    group_df = drop_highly_correlated_features(group_df)
    
    # If the property type is 'apartment' and the DataFrame has a column 'Garden area', drop it
    if property_type == 'apartment':
        if 'Garden area' in group_df.columns:
            group_df = group_df.drop(columns=['Garden area'])

    # Fill any NaN values in the DataFrame with 0
    group_df = group_df.fillna(0)
    
    # Return the preprocessed DataFrame
    return group_df


def filter_data(group_df, property_type, region):
    """
    Filters a DataFrame based on restrictions for the given property type and region.

    The function applies the restrictions defined in get_property_restrictions function to the input DataFrame. 
    It removes the properties which have living area and price values that exceed the defined restrictions.

    Parameters:
    group_df (pandas.DataFrame): The DataFrame containing property data to filter.
    property_type (str): The type of the property ('apartment' or 'house').
    region (str): The region of the property.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """
    # Get the dictionary of property restrictions
    property_restrictions = get_property_restrictions()

    # If the property type and region combination exists in the restrictions
    if (property_type, region) in property_restrictions:
        # Get the specific restrictions for the property type and region
        restrictions = property_restrictions[(property_type, region)]

        # Apply the restrictions to the DataFrame, only keeping rows where the living area and price
        # do not exceed the maximum defined in the restrictions
        group_df = group_df[(group_df['Living area'] <= restrictions['Living area']) &
                            (group_df['Price of property in euro'] <= restrictions['Price of property in euro'])]

    # Return the filtered DataFrame
    return group_df


def get_property_restrictions():
    """
    Returns a dictionary containing property restrictions for different types of properties in different regions.

    Each key in the dictionary is a tuple (property_type, region), and the value is another dictionary 
    that specifies the maximum allowable 'Living area' and 'Price of property in euro' for properties of 
    that type in that region. This dictionary can be used to filter properties based on these restrictions.

    Parameters:
    None

    Returns:
    dict: A dictionary with restrictions for different property types in different regions.
    """

    # Define the dictionary of property restrictions
    restrictions = {
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

    return restrictions

