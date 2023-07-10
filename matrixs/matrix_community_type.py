import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("property_data.csv")

#Step 1 : Data Cleaning

#Removing duplicates
df = df.drop_duplicates()

#Removing leading and trailing spaces
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# fill missing values with a specific value
df = df.fillna("0")

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

# Calculate the correlation matrix of the numeric columns for the whole Belgium and each community and type of property
for (community, type_of_property), group_df in df.groupby(['Community', 'Type of property']):
    # If the type_of_property is '0', skip the current iteration
    if type_of_property == '0':
        continue

    print(f"Community: {community}, Type of property: {type_of_property}")

    # Use a different set of numeric columns for apartments and houses
    if type_of_property == 'apartment':
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Number of facades']
    else:
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Surface of the land(or plot of land)', 'Number of facades', 'Swimming pool']
    
    corr = group_df[numeric_cols].corr()
    fig = px.imshow(corr, title=f"Correlation matrix beetween price and variables in {community} for {type_of_property}", zmin=-1, zmax=1)
    fig.show()



