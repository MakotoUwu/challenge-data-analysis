import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("property_data.csv")

#Step 1 : Data Cleaning

#Removing duplicates
df = df.drop_duplicates()

#Removing leading and trailing spaces
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Calculating percentage of missing data in each column
missing_percentage = df.isnull().sum() * 100 / len(df)
print("Percentage of missing data in each column: ")
print(missing_percentage)

# fill missing values with a specific value
df.loc[:, df.dtypes == np.float64] = df.loc[:, df.dtypes == np.float64].fillna(0)
df.loc[:, df.dtypes == np.int64] = df.loc[:, df.dtypes == np.int64].fillna(0)
df.loc[:, df.dtypes == object] = df.loc[:, df.dtypes == object].fillna('unknown')
print(df.head())

#Step 2 : Data Analysis

# Get the number of rows and columns using df.shape
rows, cols = df.shape
print(f"The dataset has {rows} rows and {cols} columns.")

#better to make one for belgium and

def get_region(zip_code):
    if 1000 <= zip_code <= 1299:
        return 'Brussels-Capital Region'
    elif 1300 <= zip_code <= 1499:
        return 'Province of Walloon Brabant'
    elif (1500 <= zip_code <= 1999) or (3000 <= zip_code <= 3499):
        return 'Province of Flemish Brabant'
    elif 2000 <= zip_code <= 2999:
        return 'Province of Antwerp'
    elif 3500 <= zip_code <= 3999:
        return 'Province of Limburg'
    elif 4000 <= zip_code <= 4999:
        return 'Province of Liege'
    elif 5000 <= zip_code <= 5999:
        return 'Province of Namur'
    elif (6000 <= zip_code <= 6599) or (7000 <= zip_code <= 7999):
        return 'Province of Hainaut'
    elif 6600 <= zip_code <= 6999:
        return 'Province of Luxembourg'
    elif 8000 <= zip_code <= 8999:
        return 'Province of West Flanders'
    elif 9000 <= zip_code <= 9999:
        return 'Province of East Flanders'


# Ensure that the 'Zip code' column is in integer format
df['Zip code'] = df['Zip code'].astype(int)

# Map the 'Zip code' column to regions
df['Region'] = df['Zip code'].apply(get_region)

# Calculate the correlation matrix of the numeric columns within each region and type of property
for (region, type_of_property), group_df in df.groupby(['Region', 'Type of property']):
    print(f"Region: {region}, Type of property: {type_of_property}")

    # Use a different set of numeric columns for apartments and houses
    if type_of_property == 'apartment':
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Number of facades']
    else:
        numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Surface of the land(or plot of land)', 'Number of facades', 'Swimming pool']
    
    corr = group_df[numeric_cols].corr()
    fig = px.imshow(corr, title=f"Correlation matrix of variables and price in {region} for {type_of_property}", zmin=-1, zmax=1)
    fig.show()


