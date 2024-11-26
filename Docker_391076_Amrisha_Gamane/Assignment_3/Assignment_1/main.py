"""
RUN THE FAST API SERVER USING

uvicorn main:app --reload
"""

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("winequality-red.csv")

class WineDataFilter:
    def __init__(self, df):
        self.df = df

    def filter_by_quality(self, quality):
        filtered_df = self.df[self.df['quality'] == quality]
        return filtered_df

    def get_feature_distribution(self, feature, quality):
        filtered_df = self.filter_by_quality(quality)
        return filtered_df[feature]

app = FastAPI()


app.mount("/images", StaticFiles(directory="images"), name="images")

wine_data_filter = WineDataFilter(df)

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
    <head>
        <title>Welcome to the Wine Quality API</title>
    </head>
    <body>
        <h1>Welcome to the Wine Quality API</h1>
        <p>You can see the filtered data by logging on to <a href="/filter_wine?quality=5">/filter_wine?quality=5</a></p>
        <p>And see the visualizations on <a href="/visualize_feature?quality=5&feature=alcohol">/visualize_feature?quality=5&feature=alcohol</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/filter_wine", response_class=HTMLResponse)
def filter_wine(quality: int):
    filtered_data = wine_data_filter.filter_by_quality(quality)
    
    html_table = filtered_data.to_html(classes='table table-striped', index=False)
    
    html_content = f"""
    <html>
    <head>
        <title>Filtered Wine Data</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1>Filtered Wine Data (Quality: {quality})</h1>
            {html_table}
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/visualize_feature", response_class=HTMLResponse)
def visualize_feature(quality: int, feature: str):
    feature_distribution = wine_data_filter.get_feature_distribution(feature, quality)
    
    plt.figure(figsize=(10, 6))
    plt.hist(feature_distribution, bins=20, color='blue', edgecolor='black')
    plt.title(f'Distribution of {feature} for Quality {quality}')
    plt.xlabel(f'{feature}')
    plt.ylabel('Frequency')
    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    image_filename = f"{feature}_distribution_quality_{quality}.png"
    image_path = f"images/{image_filename}"
    plt.savefig(image_path)
    plt.close()
    

    html_content = f"""
    <html>
    <head>
        <title>Feature Distribution</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1>Distribution of {feature} for Quality {quality}</h1>
            <img src="/images/{image_filename}" alt="Feature Distribution" class="img-fluid">
            <br>
            <a href="/images/{image_filename}" download="{image_filename}" class="btn btn-primary mt-3">Save Image</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


