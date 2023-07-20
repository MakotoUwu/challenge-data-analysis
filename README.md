# Challenge-data-analysis
This repository is created for the data analysis challenge by ImmoEliza. The aim of this challenge is to analyze a dataset that contains real estate sales data and price predictions for properties in Belgium. 🏠

## Table of Contents
1. [Description](#description) 📄
2. [Installation](#installation) 💻
3. [Usage](#usage) 🛠️
4. [Visuals](#visuals) 🖼️
5. [Files and Directories](#files) 📂
6. [Contributors](#contributors) 👥
7. [Timeline](#timeline) 🗓️
8. [Personal Situation](#personal_situation) 🛂
9. [Future Improvements/Additions](#Future_Improvements/Additions) 🔜


<a name="description"></a>
## Description

The goal of this project is to provide ImmoEliza with the insights they need to establish themselves as the biggest real estate company in Belgium. By analyzing the data, I aim to answer questions related to the correlation between various variables and the property price, the most and least expensive municipalities in Belgium, and other related questions.

The project involves extensive data cleaning, data analysis using tools such as pandas, matplotlib and seaborn, and presenting the interpreted results using simple words and relevant visuals.

In my opinion the most important variables are:
- Living area: This is the total living area of the property in square meters. It seems obvious that this would have a strong influence on the price, as larger properties tend to be more expensive than smaller ones. This variable also has a high correlation with price in the dataset.
- Rooms: This is the number of rooms in the property. This could also affect the price, as more rooms could mean more space, comfort and functionality. This variable also has a moderate correlation with price in the dataset.
- Region: There are three regions in Belgium: Brussels-Capital Region, Flemish Region and Walloon Region. This variable could have an impact on the price, as different regions could have different levels of demand, supply, income, taxes, etc. This variable also shows some variation in price per square meter across regions in the dataset.
- Type: This is the type of property, such as house, apartment, villa, etc. This variable could also influence the price, as different types of properties could have different features, qualities and preferences. This variable also shows some variation in price per square meter across types in the dataset.
- Price


<a name="installation"></a>
## Installation

The project requires Python 3.7+ and the following Python libraries installed:

- NumPy
- Pandas
- matplotlib
- Seaborn
- Plotly
- Scikit-learn

To install any missing dependencies, use pip:

```pip install -r requirements.txt```

<a name="usage"></a>
## Usage

All expalinig you can find in ipynb files. Run each notebook from the terminal or command line:

```ipython notebook <name_of_notebook.ipynb>```

<a name="visuals"></a>
## Visuals

All the visuals can be found in the respective Jupyter notebooks. Ex:

![My Image](output/output.png)
![My Image](output/newplot.png)
![My Image](output/predict.png)
![My Image](output/predict2.png)

<a name="files"></a>
## Files and Directories

1. `/data`:
    - `property_data.csv`: This file contains the raw dataset for the project. 
2. `/data-exploration`:
    - `Bel_mean_medium_price.ipynb`: This notebook shows plots for Mean, median, and price per meter for properties in Belgium. 
    - `subtype_of_property_vs_price.ipynb`: This Jupyter notebook contains a visualization showing the relationship between the price and each subtype of properties.
    - `Fla_mean_medium_price.ipynb`: This notebook shows plots for Mean, median, and price per meter for properties in Flanders.
    - `Wal_mean_medium_price.ipynb`: This notebook shows plots for Mean, median, and price per meter for properties in Wallonia.  
    - `matrix_Belgium.ipynb`: This notebook contains a heatmap matrix correlation between price and variables in Belgium.
    - `matrix_Regions.ipynb`: This notebook contains a heatmap matrix correlation between price and variables in every region in Belgium.  
    - `represent_surface_histogram.ipynb`: This Jupyter notebook contains a histogram representing the number of properties according to their surface.
3. `/model-building`:
    - `model_building.ipynb`: This notebook contains a complete data analysis pipeline, which involves data preprocessing, training machine learning models, and visualizing the model's performance for predicting property prices across different property types and regions.
4. `/src`:
    - `data_preprocessing.py`: This script handles data loading, cleaning, and preprocessing for property data analysis and model training.
    - `data_visualization.py`: This script shows plots which predicted property prices based on 'Living area' using Linear Regression.
    - `model_training.py`: This script fits, predicts, and evaluates Linear Regression and XGBoost models on property data, handling model training, performance metrics calculation, and data split/scaling.
5. `/output`: This folder contains examples various graphical representations and plots generated from the data analysis, providing visual insights into property prices and model performances.
6. `README.md`: Contain all instracture
6. `requirements.txt`: This file lists all of the Python libraries that your system needs to run the notebooks.


<a name="contributors"></a>
## Contributors

[Oleksandr Tsepukh (Junior Data Scientist at BeCode)](https://www.linkedin.com/in/oleksandr-tsepukh-ba4985279)

<a name="timeline"></a>
## Timeline

The challenge was completed in 5 days from (06/07/2023) to (11/07/2023)

<a name="personal_situation"></a>
## Personal Situation

As a student at BeCode in Ghent, this project presented an opportunity to apply and strengthen my data analysis skills. From meticulous data cleaning to strategic data interpretation, every step was a learning experience. Despite the challenges, I successfully utilized Python libraries like pandas, scikit-learn, matplotlib, and seaborn to derive meaningful insights from the data. This project was a significant milestone in my data analysis journey, reinforcing my analytical capabilities and passion for the field.

This project is part of the AI Bootcamp at BeCode.org

<a name="Future_Improvements/Additions"></a>
## Future Improvements/Additions 

- Making more reaserching in every region to make model fit well