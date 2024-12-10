import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Next Days")
city = st.text_input("City: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky", "Humidity", "Pressure", "Wind Speed", "UV Index", "Visibility", "Cloud Coverage"))
st.subheader(f"{option} for the next {days} days in {city}")

# Get the weather data
if city:
    try:
        filtered_data = get_data(city, days)

        if option == "Temperature":
            # Convert temperature from Kelvin to Celsius
            temperatures = [data["main"]["temp"] - 273.15 for data in filtered_data]  # Kelvin to Celsius conversion
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
            st.plotly_chart(figure)

        elif option == "Humidity":
            humidity = [data["main"]["humidity"] for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.bar(x=dates, y=humidity, labels={"x": "Date", "y": "Humidity (%)"})
            st.plotly_chart(figure)

        elif option == "Pressure":
            pressure = [data["main"]["pressure"] for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=pressure, labels={"x": "Date", "y": "Pressure (hPa)"})
            st.plotly_chart(figure)

        elif option == "Wind Speed":
            wind_speed = [data["wind"]["speed"] for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=wind_speed, labels={"x": "Date", "y": "Wind Speed (m/s)"})
            st.plotly_chart(figure)

        elif option == "Visibility":
            visibility = [data["visibility"] / 1000 for data in filtered_data]  # Convert meters to kilometers
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=visibility, labels={"x": "Date", "y": "Visibility (km)"})
            st.plotly_chart(figure)

        elif option == "Cloud Coverage":
            cloud_coverage = [data["clouds"]["all"] for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=cloud_coverage, labels={"x": "Date", "y": "Cloud Coverage (%)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            images = {
                "Clear": "images/clear1.jpg",
                "Clouds": "images/cloud1.jpg",
                "Rain": "images/rain1.jpg",
                "Snow": "images/snow1.jpg"
            }
            sky_conditions = [data["weather"][0]["main"] for data in filtered_data]
            image_paths = [images.get(condition, "images/default.png") for condition in sky_conditions]
            
            # Display the images in a grid layout
            max_columns = 5  # Max columns in a row
            max_rows = 3     # Max rows
            total_images = len(image_paths)
            
            # Create a grid with a maximum of 3 rows and 5 columns
            cols = st.columns(max_columns)
            
            # Create the grid
            for i in range(0, total_images, max_columns):
                row_images = image_paths[i:i + max_columns]  # Get a subset of images for this row
                row_cols = st.columns(len(row_images))  # Create as many columns as the number of images in this row
                
                for col, image_path in zip(row_cols, row_images):
                    col.image(image_path, width=90)  # Display each image in the respective column

    except KeyError:
        st.error("Invalid city name or data unavailable. Please try again.")
