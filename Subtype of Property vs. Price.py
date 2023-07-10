import pandas as pd
import plotly.express as px

df = pd.read_csv("property_data.csv")

# Step 1: Data Cleaning
df = df.drop_duplicates()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Fill missing values with a specific value
df = df.fillna({'Price of property in euro': 0, 'Zip code': 0, 'Subtype of property': 'unknown'})

# Step 2: Data Analysis
df['Price of property in euro'] = pd.to_numeric(df['Price of property in euro'], errors='coerce')
df['Zip code'] = pd.to_numeric(df['Zip code'], errors='coerce')
df = df.dropna(subset=['Price of property in euro', 'Zip code'])

# Step 2: Data Analysis
sorted_subtypes = df.groupby('Subtype of property')['Price of property in euro'].max().sort_values(ascending=False).index

fig = px.box(df, x='Subtype of property', y='Price of property in euro', category_orders={"Subtype of property": sorted_subtypes}, color='Subtype of property')
fig.update_layout(
    title="Box Plot: Subtype of Property vs. Price of Property in Euro (Sorted by Highest Price)",
    xaxis_title="Subtype of Property",
    yaxis_title="Price of Property in Euro",
    boxmode='group'  # Grouped box plots
)
fig.show()
