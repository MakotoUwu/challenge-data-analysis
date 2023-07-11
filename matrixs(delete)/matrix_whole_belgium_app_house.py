import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("property_data.csv")

#Step 1 : Data Cleaning

#Removing duplicates
df = df.drop_duplicates()

#Removing leading and trailing spaces
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# fill missing values in numeric columns with appropriate value
df.loc[:, df.dtypes == np.float64] = df.loc[:, df.dtypes == np.float64].fillna(0)
df.loc[:, df.dtypes == np.int64] = df.loc[:, df.dtypes == np.int64].fillna(0)

# fill missing values in non-numeric columns with 'unknown'
df.loc[:, df.dtypes == object] = df.loc[:, df.dtypes == object].fillna('unknown')

rows, cols = df.shape
print(f"The dataset has {rows} rows and {cols} columns.")

# Ensure that the 'Zip code' column is in integer format
df['Zip code'] = df['Zip code'].astype(int)

# Ensure 'Subtype of property' is a string
df['Subtype of property'] = df['Subtype of property'].astype(str)

# One-hot encode 'Subtype of property'
df_encoded = pd.get_dummies(df, columns=['Subtype of property'])

# Ensure 'Type of Sale' is a string
df['Type of Sale'] = df['Type of Sale'].astype(str)

# One-hot encode 'Type of Sale'
df_encoded = pd.get_dummies(df_encoded, columns=['Type of Sale'])

# Ensure 'State of the building' is a string
df['State of the building'] = df['State of the building'].astype(str)

# One-hot encode 'State of the building'
df_encoded = pd.get_dummies(df_encoded, columns=['State of the building'])

for type_of_property, group_df in df_encoded.groupby('Type of property'):
    # If the type_of_property is '0' or 'unknown', skip the current iteration
    if type_of_property == '0' or type_of_property.lower() == 'unknown':
        continue

    print(f"Type of property: {type_of_property}")

    # Use a different set of numeric columns for apartments and houses
    if type_of_property == 'apartment':
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Number of facades']
    else:
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Surface of the land(or plot of land)', 'Number of facades', 'Swimming pool']

    # Add the encoded 'Subtype of property', 'Type of Sale', and 'State of the building' columns
    for col in group_df.columns:
        if 'Subtype of property_' in col or 'Type of Sale: ' in col or 'State of the building: ' in col:
            numeric_cols.append(col)

    corr = group_df[numeric_cols].corr()
    fig = px.imshow(corr, title=f"Correlation matrix between price and variables for {type_of_property} in Belgium", zmin=-1, zmax=1)
    fig.show()
