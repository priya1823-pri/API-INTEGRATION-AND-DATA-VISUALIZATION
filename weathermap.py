import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sys
import requests

# -------------------------------
# CONFIGURATION
# -------------------------------
API_KEY = "fdabb77a6a6d216b9e388decfe601ff1"  # Your API key
CITY = "Bengaluru"
UNITS = "metric"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"  # ✅ FIXED

# -------------------------------
# FETCH DATA FROM API
# -------------------------------
def fetch_weather_data(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": UNITS
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

# -------------------------------
# PROCESS DATA INTO DATAFRAME
# -------------------------------
def process_weather_data(data):
    try:
        records = []
        for entry in data["list"]:  # ✅ Now valid
            records.append({
                "datetime": datetime.fromtimestamp(entry["dt"]),
                "temperature": entry["main"]["temp"],
                "humidity": entry["main"]["humidity"],
                "pressure": entry["main"]["pressure"],
                "weather": entry["weather"][0]["description"]
            })
        df = pd.DataFrame(records)
        return df
    except (KeyError, TypeError) as e:
        print(f"Error processing data: {e}")
        sys.exit(1)

# -------------------------------
# CREATE VISUALIZATION DASHBOARD
# -------------------------------
def create_dashboard(df, city):
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    sns.lineplot(ax=axes[0], x="datetime", y="temperature", data=df, marker="o")
    axes[0].set_title(f"Temperature Trend in {city}")
    axes[0].set_ylabel("Temperature (°C)")

    sns.lineplot(ax=axes[1], x="datetime", y="humidity", data=df, marker="o")
    axes[1].set_title("Humidity Trend")
    axes[1].set_ylabel("Humidity (%)")

    sns.lineplot(ax=axes[2], x="datetime", y="pressure", data=df, marker="o")
    axes[2].set_title("Pressure Trend")
    axes[2].set_ylabel("Pressure (hPa)")
    axes[2].set_xlabel("Date & Time")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":
    print(f"Fetching weather data for {CITY}...")
    raw_data = fetch_weather_data(CITY)
    df_weather = process_weather_data(raw_data)
    print(df_weather.head())
    create_dashboard(df_weather, CITY)
