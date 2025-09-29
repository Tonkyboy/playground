import tkinter as tk
from tkinter import messagebox
import urllib.request
import json

weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        95: "Thunderstorm"
    }

def get_weather(city):
    # Geocode city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        with urllib.request.urlopen(geo_url) as response:
            geo_data = json.loads(response.read().decode())
            if geo_data['results']:
                lat = geo_data['results'][0]['latitude']
                lon = geo_data['results'][0]['longitude']
                # Fetch weather
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                with urllib.request.urlopen(weather_url) as w_response:
                    weather_data = json.loads(w_response.read().decode())
                    current = weather_data['current_weather']
                    code = current['weathercode']
                    weather_desc = weather_codes.get(code, "Unknown")
                    return f"Temperature: {current['temperature']}°C\nWeather: {weather_desc}"
            else:
                return "City not found."
    except Exception as e:
        return f"Error: {str(e)}"

def on_submit():
    city = entry.get()
    if city:
        result = get_weather(city)
        label.config(text=result)
        print(result)
    else:
        messagebox.showwarning("Input", "Enter a city!")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

tk.Label(root, text="Enter city:").pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=on_submit).pack(pady=10)

label = tk.Label(root, text="", justify=tk.LEFT)
label.pack(pady=10)

root.mainloop()
    
