# 🌎 Climate Hub

**Climate Hub** is a sleek, Streamlit-based weather application that provides **today’s weather** and a **7-day forecast** for cities across Pakistan.  
It uses **Open-Meteo** for accurate weather data and **Nominatim (OpenStreetMap)** for city coordinates — all completely free and without any API keys.


## 🚀 Features

- ☀️ **Today’s Weather** — Shows real-time temperature, condition, and icon.  
- 📅 **7-Day Forecast** — Beautiful forecast cards with icons, max/min temperatures, and day names.  
- 🧭 **City Selection** — Choose from major Pakistani cities like Lahore, Karachi, Islamabad, etc.  
- 💾 **Session Handling** — Keeps weather and forecast data after button clicks.  
- 🎨 **Modern UI** — Responsive weather cards with emojis and clean visuals.  
- ⚡ **Free APIs** — Uses Open-Meteo and Nominatim (no keys or paid plans needed).  

## 🛠️ Tech Stack
- Python 3.13+

- Streamlit – For interactive web UI

- Requests – For API calls

- Open-Meteo API – Weather data

- Nominatim API (OpenStreetMap) – City geocoding


## Project structure
```
Climate-Hub/
│
├── app.py                  # Main Streamlit app
├── weather_api.py          # API functions: coordinates, current weather, 7-day forecast
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore file (ignore .venv, __pycache__, etc.)
└── .venv/                  # Virtual environment (optional, local setup)
```

## 📦 Installation & Setup

Follow these steps to set up and run **Climate Hub** locally 👇  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Climate-Hub.git
cd Climate-Hub
```

### 2️⃣ Create and Activate Virtual Environment
```
python -m venv .venv
.venv\Scripts\activate      # On Windows
# source .venv/bin/activate  # On macOS/Linux
```
### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Run the App
```
streamlit run app.py
```
### 5️⃣ Open in Browser
```
Once the server starts, Streamlit will automatically open your default browser.
If not, visit 👉 http://localhost:8501
```

## 💡 How It Works
- User selects a city (e.g., Lahore).

- On clicking “Today’s Weather”, the app fetches:

- city coordinates from Nominatim

- Current temperature, condition, and icon from Open-Meteo

- The user can then click “Next 7 Days Forecast” to view:

- 7-day temperature highs/lows

- Daily weather conditions with icons

- Data is shown in beautiful, responsive weather cards.


## 👨‍💻 Author Info
- Developed by: Zain Abbas
- LinkedIn: linkedin.com/in/zainabbas-se

```
“A simple, free, and beautiful way to explore Pakistan’s weather.”
```