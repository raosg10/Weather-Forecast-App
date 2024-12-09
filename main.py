import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Next Days")
city = st.text_input("City: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {city}")

# Get the temperature/sky data
if city:
    try:
        filtered_data = get_data(city, days)

        if option == "Temperature":
            # Create temperature plot
            temperatures = [data["main"]["temp"]-273.15 for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            images = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png"
            }
            sky_conditions = [data["weather"][0]["main"] for data in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
             # Define number of rows and columns for the 3x5 grid
            max_columns = 5  # Max columns in a row
            max_rows = 10     # Max rows
            total_images = len(image_paths)
            
            # Create a grid with a maximum of 3 rows and 5 columns
            cols = st.columns(max_columns)
            
            # Create the grid
            for i in range(0, total_images, max_columns):
                row_images = image_paths[i:i + max_columns]  # Get a subset of images for this row
                row_cols = st.columns(len(row_images))  # Create as many columns as the number of images in this row
                
                for col, image_path in zip(row_cols, row_images):
                    col.image(image_path, width=115)  # Display each image in the respective column

    except KeyError:
        st.error("Invalid city name or data unavailable. Please try again.")
