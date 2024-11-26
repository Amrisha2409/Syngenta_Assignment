import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px

# Configure the page
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# API configuration
API_KEY = "6f40f87e32a28866983fb5dea5ca0f11"  # Hardcoding for testing
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather data with debug information"""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    # Debug information
    full_url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    st.write("Debug Info:")
    st.write(f"Using API Key: {API_KEY}")
    st.write(f"Requesting URL: {full_url}")
    
    try:
        response = requests.get(BASE_URL, params=params)
        st.write(f"Response Status Code: {response.status_code}")
        st.write(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            st.write(f"Error Response Text: {response.text}")
            
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def main():
    st.title("🌤️ Weather Dashboard")
    
    # Input for city
    city = st.text_input("Enter City Name", "Pune")
    
    if st.button("Get Weather"):
        if city:
            weather_data = get_weather_data(city)
            
            if weather_data:
                # Display current conditions
                st.markdown(f"""
                    <div style="
                        background-color: white;
                        padding: 1.5rem;
                        border-radius: 15px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                        margin: 1rem 0;
                        text-align: center;
                    ">
                        <h2 style="color: #5c8d89; margin-bottom: 1rem;">
                            Current Weather in {city.title()}
                        </h2>
                        <p style="font-size: 1.2rem; color: #2c5530;">
                            {weather_data['weather'][0]['description'].capitalize()}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                # Create three columns for main metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Temperature", f"{weather_data['main']['temp']}°C")
                with col2:
                    st.metric("Humidity", f"{weather_data['main']['humidity']}%")
                with col3:
                    st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")

                # Create visualization
                weather_metrics = pd.DataFrame({
                    'Metric': ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)'],
                    'Value': [
                        weather_data['main']['temp'],
                        weather_data['main']['humidity'],
                        weather_data['wind']['speed']
                    ]
                })
                
                fig = px.bar(
                    weather_metrics,
                    x='Metric',
                    y='Value',
                    title='Weather Metrics Visualization',
                    color_discrete_sequence=['#9dc88d']
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#5c8d89',
                    font_color='#2c5530'
                )
                
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Please enter a city name")

if __name__ == "__main__":
    main()