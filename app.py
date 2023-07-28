from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel, Field, validator
from typing import Literal
from fastapi.responses import JSONResponse
import pickle
import numpy as np
import os

# Initialize FastAPI app
app = FastAPI()

# Define the list of valid regions
valid_regions = [
    "Brussels-Capital", 
    "Walloon Brabant", 
    "Flemish Brabant", 
    "Antwerp", 
    "Limburg", 
    "Liege", 
    "Namur", 
    "Hainaut", 
    "Luxembourg", 
    "West Flanders", 
    "East Flanders"
]

# Define Pydantic model to validate the incoming request data
class Data(BaseModel):
    type_of_property: Literal['house', 'apartment'] = Field(..., description="Type of property, must be either 'house' or 'apartment'.")
    number_of_bedrooms: float = Field(..., ge=0, description="Number of bedrooms. Must be non-negative.")
    living_area: float = Field(..., ge=0, description="Living area in square meters. Must be non-negative.")
    terrace_area: float = Field(..., ge=0, description="Terrace area in square meters. Must be non-negative.")
    surface_of_land: float = Field(..., ge=0, description="Surface area of land in square meters. Must be non-negative.")
    number_of_facades: float = Field(..., ge=0, description="Number of facades. Must be non-negative.")
    region: str = Field(..., description="Region where the property is located.")

    # Validator for region field
    @validator('region')
    def validate_string(cls, value):
        if not isinstance(value, str) or value not in valid_regions:
            raise ValueError(f"Invalid region. Must be one of {', '.join(valid_regions)}.")
        return value

# Define a root ("/") GET endpoint 
@app.get("/")
def read_root():
    # Return a welcome message
    return {"message": "Welcome to our real estate prediction API! You can make a POST request to /predict with the necessary property details to get a prediction."}

# Define a predict ("/predict") POST endpoint 
@app.post("/predict", status_code=201)
def predict_price(
    type_of_property: Literal['house', 'apartment'] = Form(...),
    number_of_bedrooms: float = Form(...),
    living_area: float = Form(...),
    terrace_area: float = Form(...),
    surface_of_land: float = Form(...),
    number_of_facades: float = Form(...),
    region: str = Form(...)
):
    # Create a data object from the form fields
    property = Data(
        type_of_property=type_of_property,
        number_of_bedrooms=number_of_bedrooms,
        living_area=living_area,
        terrace_area=terrace_area,
        surface_of_land=surface_of_land,
        number_of_facades=number_of_facades,
        region=region
    )

    # Define the model path
    model_path = f'./models/{property.type_of_property}_{property.region}_model.pickle'

    # Check if the model file exists
    if not os.path.exists(model_path):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"No model found for property type '{property.type_of_property}' and region '{property.region}'. Please ensure that you have selected a valid region and property type."
            }
        )

    try:
        # Load the model using pickle
        model = pickle.load(open(model_path, 'rb'))

        # Define the feature names that are expected by the model
        feature_names = ['number_of_bedrooms', 'living_area', 'terrace_area', 'surface_of_land', 'number_of_facades']

        # Extract features from the incoming request data
        features = np.array([property.dict()[feat] for feat in feature_names])

        # Reshape the features to match the input shape that the model expects
        features = features.reshape(1, -1)

        # Make prediction using the model
        prediction = model.predict(features)

        # Return the prediction in the response
        return {"prediction": float(prediction[0])}

    except Exception as e:
        # If anything goes wrong during prediction, return a 500 error with the details of the exception
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"An error occurred during prediction: {str(e)}. Please try again."
            }
        )
