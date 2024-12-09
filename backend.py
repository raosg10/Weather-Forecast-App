import requests
import os

# Get your API key from environment variables or hardcode it securely.
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "ab1f74adba83eff8df8dff9360e619b7")  # Better to use an env variable

def get_data(city, forecast_days=3):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
        
        # Parse the response JSON
        data = response.json()
        
        # Filter out the forecast data for the given number of days
        filtered_data = data["list"]
        nr_values = 8 * forecast_days  # 8 data points per day
        filtered_data = filtered_data[:nr_values]
        
        return filtered_data
    
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        print(f"Error fetching data: {e}")
        return []  # Return empty list if there's an error

# For testing the backend when running directly
if __name__ == "__main__":
    print(get_data(city="Darmstadt", forecast_days=3))
