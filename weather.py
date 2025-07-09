import requests
from PIL import Image, ImageTk
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, Label, Frame, OptionMenu
import io

API_KEY = "37f7dd10933479acb36ab50637ec3f89"

def get_weather(city, unit):
    unit_param = "metric" if unit == "Celsius" else "imperial"
    unit_symbol = "°C" if unit == "Celsius" else "°F"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_param}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            result_label.config(text=f"❌ {data['message']}")
            icon_label.config(image="")
            return

        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        icon_id = data["weather"][0]["icon"]

        result_label.config(
            text=(
                f"📍 {city.title()}\n\n"
                f"{weather}\n\n"
                f"🌡 Temperature: {temp}{unit_symbol}\n"
                f"🤒 Feels like: {feels_like}{unit_symbol}\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind} m/s"
            )
        )
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@4x.png"
        icon_response = requests.get(icon_url)
        img_data = icon_response.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((100, 100))
        icon_image = ImageTk.PhotoImage(img)
        icon_label.config(image=icon_image)
        icon_label.image = icon_image

    except Exception as e:
        result_label.config(text=f"❌ Error: {e}")
        icon_label.config(image="")

def search():
    city = city_entry.get().strip()
    unit = unit_var.get()
    if not city:
        result_label.config(text="⚠️ Please enter a city name.")
        return
    get_weather(city, unit)

style = Style(theme="minty")  
app = style.master
app.title("🌤 Weather Forecast")
app.geometry("420x550")
app.configure(bg="#dfe9f3")  
frame = Frame(app, padding=20, bootstyle="light", borderwidth=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center")
Label(frame, text="Weather App", font=("Helvetica", 18, "bold"), bootstyle="primary").pack(pady=10)
Label(frame, text="City Name:", font=("Arial", 12)).pack(anchor="w")
city_entry = Entry(frame, font=("Arial", 12), width=28)
city_entry.pack(pady=5)
unit_var = tk.StringVar(value="Celsius")
Label(frame, text="Select Unit:", font=("Arial", 12)).pack(anchor="w", pady=(10, 0))
OptionMenu(frame, unit_var, "Celsius", "Fahrenheit").pack(pady=5)
Button(frame, text="Get Weather", command=search, bootstyle="success", width=25).pack(pady=15)
icon_label = Label(frame)
icon_label.pack(pady=5)
result_label = Label(frame, font=("Arial", 12), wraplength=300, justify="center")
result_label.pack(pady=10)

app.mainloop()
