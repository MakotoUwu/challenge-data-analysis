import pandas as pd
import plotly.express as px

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

# Select only the numeric columns
numeric_cols = ['Price of property in euro', 'Kitchen', 'Number of bedrooms', 'Living area', 'Terrace area', 'Garden', 'Garden area', 'Surface of the land(or plot of land)', 'Number of facades','Swimming pool']

# Calculate the correlation matrix of the numeric columns
corr = df[numeric_cols].corr()

# Plot a heatmap of the correlation matrix using plotly.express
fig = px.imshow(corr, title="Correlation Matrix of Variables and Price", zmin=-1, zmax=1)
fig.show()
