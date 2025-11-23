import streamlit as st
from weather_api import (
    get_coordinates, get_current_weather, 
    get_weather_icon, get_weather_text, get_5day_forecast
)

st.set_page_config(page_title="Climate Hub", page_icon="🌤️")
st.title("🌎 Climate Hub")
st.subheader("Check the current weather in any city of Pakistan")

# Session state for buttons
if 'show_forecast' not in st.session_state:
    st.session_state.show_forecast = False
if 'weather_loaded' not in st.session_state:
    st.session_state.weather_loaded = False

cities = ["Lahore", "Karachi", "Islamabad", "Quetta", "Peshawar", "Multan", "Faisalabad", "Sialkot"]
city = st.selectbox("Select a city", cities)

# Get Weather Button
if st.button("Get Weather"):
    with st.spinner(f"Fetching coordinates for {city}..."):
        lat, lon = get_coordinates(city)
    if lat and lon:
        st.session_state.lat = lat
        st.session_state.lon = lon
        with st.spinner("Fetching weather data..."):
            weather = get_current_weather(lat, lon)
        if weather:
            icon = get_weather_icon(weather['weathercode'])
            description = get_weather_text(weather['weathercode'])
            temperature = weather['temperature']
            wind_speed = weather['windspeed']
            
            # Display current weather in a card
            st.markdown(
                f"""
                <div style='background-color:#e0f7fa; border-radius:10px; padding:15px; text-align:center; margin:15px auto; max-width:400px'>
                    <h3 style='margin:5px 0; font-size:20px'>{icon} Current Weather in {city}</h3>
                    <p style='font-size:40px; margin:5px 0'>{icon}</p>
                    <p style='font-size:18px; font-weight:bold; margin:5px 0'>{description}</p>
                    <p style='font-size:28px; font-weight:bold; margin:8px 0'>🌡️ {temperature}°C</p>
                    <p style='font-size:14px; margin:5px 0'>💨 Wind Speed: {wind_speed} km/h</p>
                </div>
                """, unsafe_allow_html=True
            )
            st.session_state.weather_loaded = True
            st.session_state.show_forecast = False  # Reset forecast display
        else:
            st.error("Weather data not available! Please try again later.")
            st.session_state.weather_loaded = False
    else:
        st.error(f"Could not find coordinates for {city}, Pakistan. Please check the city name and try again.")
        st.session_state.weather_loaded = False

# 7-Day Forecast Button - only show if weather was successfully loaded
if st.session_state.weather_loaded:
    if st.button("Show 7-Day Forecast"):
        st.session_state.show_forecast = True

# Display forecast if button was clicked
if st.session_state.show_forecast:
    if 'lat' in st.session_state and 'lon' in st.session_state:
        forecast = get_5day_forecast(st.session_state.lat, st.session_state.lon)
        if forecast:
            st.subheader("🌤 7-Day Forecast")
            cols = st.columns(7)
            for i, col in enumerate(cols):
                if i < len(forecast['time']):
                    date = forecast['time'][i]
                    # Format date to show only day name or shorter format
                    try:
                        from datetime import datetime
                        date_obj = datetime.strptime(date, "%Y-%m-%d")
                        date_display = date_obj.strftime("%a %d/%m")
                    except:
                        date_display = date[:10] if len(date) > 10 else date
                    
                    max_temp = forecast['temperature_2m_max'][i]
                    min_temp = forecast['temperature_2m_min'][i]
                    code = forecast['weathercode'][i]
                    icon = get_weather_icon(code)
                    condition = get_weather_text(code)

                    col.markdown(
                        f"""
                        <div style='background-color:#e0f7fa; border-radius:10px; padding:18px; text-align:center'>
                            <p style='font-size:16px; font-weight:bold; margin:6px 0'>{date_display}</p>
                            <p style='font-size:42px; margin:10px 0'>{icon}</p>
                            <p style='font-size:14px; margin:6px 0; word-wrap:break-word'>{condition}</p>
                            <p style='font-size:16px; margin:6px 0'>🌡️ {max_temp}°/{min_temp}°</p>
                        </div>
                        """, unsafe_allow_html=True
                    )
        else:
            st.error("7-day forecast not available!")
    else:
        st.error("Please click 'Get Weather' first!")
