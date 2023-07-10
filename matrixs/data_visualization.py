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

#better to make one for belgium and 

""" def get_region(zip_code):
    if 1000 <= zip_code < 1300:
        return 'Brussels region'
    elif 1300 <= zip_code < 1500:
        return 'Walloon Brabant region'
    elif 1500 <= zip_code < 2000:
        return 'Flemish Brabant region'
    elif 2000 <= zip_code < 3000:
        return 'Antwerp region'
    elif 3000 <= zip_code < 3500:
        return 'Flemish Brabant region'
    elif 3500 <= zip_code < 4000:
        return 'Limburg region'
    elif 4000 <= zip_code < 5000:
        return 'Liege region'
    elif 5000 <= zip_code < 6000:
        return 'Namur region'
    elif 6000 <= zip_code < 7000:
        return 'Hainaut region'
    elif 7000 <= zip_code < 8000:
        return 'Hainaut region'
    elif 8000 <= zip_code < 9000:
        return 'West Flanders region'
    elif 9000 <= zip_code <= 9999:
        return 'East Flanders region' """

def get_community(zip_code):
    if zip_code < 4000 or (5000 <= zip_code < 8000):
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
#df['Region'] = df['Zip code'].apply(get_region)
df['Community'] = df['Zip code'].apply(get_community)

# Calculate the correlation matrix of the numeric columns for the whole Belgium and each community and type of property
for (community, type_of_property), group_df in df.groupby(['Community', 'Type of property']):
    print(f"Community: {community}, Type of property: {type_of_property}")

    # Use a different set of numeric columns for apartments and houses
    if type_of_property == 'apartment':
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Number of facades']
    else:
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Surface of the land(or plot of land)', 'Number of facades', 'Swimming pool']
    
    corr = group_df[numeric_cols].corr()
    fig = px.imshow(corr, title=f"Correlation Matrix beetween Price and variables in {community} for {type_of_property}", zmin=-1, zmax=1)
    fig.show()


