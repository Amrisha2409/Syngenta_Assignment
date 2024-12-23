from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional

app = FastAPI()

class IrisDataFilter:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def filter_by_species(self, species):
        filtered_data = self.data[self.data['Species'] == species]
        return filtered_data

    def plot_feature_distribution(self, filtered_data, feature, output_file):
        plt.figure(figsize=(8, 6))
        plt.hist(filtered_data[feature], bins=10, color='blue', alpha=0.7)
        plt.title(f'Distribution of {feature} for {filtered_data["Species"].iloc[0]}')
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(output_file)
        plt.close()

iris_data_filter = IrisDataFilter(
    file_path='C:/SEM-5 Assignments/MLOPS/Iris.csv')

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Iris Data Filter API! Use /species/ to filter data and /visualize/ to get images."}

@app.get("/species/")
async def get_filtered_data(species: str, feature: Optional[str] = None):
    filtered_data = iris_data_filter.filter_by_species(species)

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Species not found")

    response = {
        "data": filtered_data.to_dict(orient="records")
    }

    if feature:
        if feature not in filtered_data.columns:
            raise HTTPException(status_code=400, detail="Feature not found in dataset.")
        
        image_path = f"{species}_{feature}_distribution.png"
        iris_data_filter.plot_feature_distribution(filtered_data, feature, image_path)

        if not os.path.exists(image_path):
            raise HTTPException(status_code=500, detail="Image generation failed")

        response["image"] = image_path

    return response

@app.get("/visualize/")
async def visualize_species(species: str, feature: str):
    image_path = f"{species}_{feature}_distribution.png"

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)
