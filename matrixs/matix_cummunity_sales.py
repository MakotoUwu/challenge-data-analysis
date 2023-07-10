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


print(df.head())

#Step 2 : Data Analysis

# Get the number of rows and columns using df.shape
rows, cols = df.shape
print(f"The dataset has {rows} rows and {cols} columns.")
 
def get_community(zip_code):
    if (1300 <= zip_code <= 1499) or (5000 <= zip_code < 8000):
        return 'Wallonia'
    elif zip_code >= 4000 and zip_code < 5000:
        return 'German-speaking community'
    elif 1000 <= zip_code < 1300:
        return 'Brussels region'
    else:
        return 'Flanders'


# Ensure that the 'Zip code' column is in integer format
df['Zip code'] = df['Zip code'].astype(int)

# Map the 'Zip code' column to regions and communities
df['Community'] = df['Zip code'].apply(get_community)

# Ensure 'Subtype of property' is a string
df['Subtype of property'] = df['Subtype of property'].astype(str)

# One-hot encode 'Subtype of property'
df_encoded = pd.get_dummies(df, columns=['Subtype of property'])

# Now, 'Subtype of property' has been one-hot encoded into multiple binary columns
# For example, if 'Subtype of property' had values 'A', 'B', 'C', now there are three new columns: 'Subtype of property_A', 'Subtype of property_B', 'Subtype of property_C'

# Ensure 'Type of Sale' is a string
df['Type of Sale'] = df['Type of Sale'].astype(str)

# One-hot encode 'Type of Sale'
df_encoded = pd.get_dummies(df, columns=['Subtype of property', 'Type of Sale'])

# Ensure 'State of the building' is a string
df['State of the building'] = df['State of the building'].astype(str)

# One-hot encode 'State of the building'
df_encoded = pd.get_dummies(df, columns=['Subtype of property', 'Type of Sale', 'State of the building'])

# Now, 'State of the building' has been one-hot encoded into multiple binary columns

for (community, type_of_property), group_df in df_encoded.groupby(['Community', 'Type of property']):
    # If the type_of_property is '0', skip the current iteration
    if type_of_property == '0':
        continue

    print(f"Community: {community}, Type of property: {type_of_property}")

    # Use a different set of numeric columns for apartments and houses
    if type_of_property == 'apartment':
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Number of facades']
    else:
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Surface of the land(or plot of land)', 'Number of facades', 'Swimming pool']

    # Add the encoded 'Subtype of property', 'Type of Sale', and 'State of the building' columns
    for col in group_df.columns:
        if 'Subtype of property_' in col or 'Type of Sale_' in col or 'State of the building_' in col:
            numeric_cols.append(col)

    corr = group_df[numeric_cols].corr()
    fig = px.imshow(corr, title=f"Correlation matrix between price and variables in {community} for {type_of_property}", zmin=-1, zmax=1)
    fig.show()
