import asyncio
import platform
import os
import httpx
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ---- Windows async fix ----
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_season(month: int) -> str:
    """Return the season based on month (northern hemisphere)."""
    if month in (12, 1, 2):
        return "winter"
    elif month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    else:
        return "autumn"

async def get_weather(latitude: float, longitude: float) -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,snowfall",
        "current_weather": "true",
        "timezone": "auto"
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Current temp + wind
            temp = data["current_weather"]["temperature"]
            wind = data["current_weather"]["windspeed"]
            current_time = data["current_weather"]["time"]

            # Hourly precipitation & snowfall
            times = data["hourly"]["time"]
            prec = data["hourly"]["precipitation"]
            snow = data["hourly"]["snowfall"]

            # Match the index of current_weather time
            if current_time in times:
                idx = times.index(current_time)
            else:
                now = datetime.utcnow()
                hour_diffs = [abs((parser.isoparse(t) - now).total_seconds()) for t in times]
                idx = hour_diffs.index(min(hour_diffs))

            precipitation = prec[idx]
            snowfall = snow[idx]

            # Build weather message
            weather_msg = f"🌡️ Temperature: {temp}°C\n💨 Wind: {wind} km/h\n"

            if snowfall > 0:
                weather_msg += "❄️ It is snowing now\n"
            elif precipitation > 0:
                weather_msg += "🌧️ It is raining now\n"
            else:
                weather_msg += "☀️ No rain or snow\n"

            # ✅ Season-aware clothing advice
            month = datetime.now().month
            season = get_season(month)
            advice = []

            if season == "winter":
                if temp < 0:
                    advice.append("🧥 Dress very warmly, it’s freezing!")
                elif temp < 10:
                    advice.append("🧣 Wear a warm jacket and maybe a scarf.")
                else:
                    advice.append("🌼 Unusually warm for winter, but still bring a jacket.")
            elif season == "spring":
                if temp < 10:
                    advice.append("🧥 Still chilly in spring — jacket needed.")
                elif temp < 20:
                    advice.append("👕 Pleasant spring weather, light clothes are fine.")
                else:
                    advice.append("😎 Warm spring day, t-shirt weather.")
            elif season == "summer":
                if temp < 15:
                    advice.append("🧥 Cool summer day, maybe a hoodie.")
                elif temp < 25:
                    advice.append("👕 Comfortable summer weather.")
                else:
                    advice.append("🔥 Very hot — stay hydrated and wear light clothes.")
            elif season == "autumn":
                if temp < 10:
                    advice.append("🧥 Cold autumn day, wear a coat.")
                elif temp < 20:
                    advice.append("🍂 Mild autumn weather, sweater recommended.")
                else:
                    advice.append("☀️ Warm autumn day, enjoy light clothes.")

            if snowfall > 0:
                advice.append("🥾 Wear boots for the snow.")
            elif precipitation > 0:
                advice.append("☂️ Better take an umbrella.")

            if wind >= 20:
                advice.append("🧢 Strong wind — wear a cap or hood.")

            if advice:
                weather_msg += "\n" + "\n".join(advice)

            return weather_msg

    except Exception as e:
        return f"Error fetching weather: {e}"

# ---- Bot Handlers ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Please share your location so I can tell you the current weather.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Send location 📍", request_location=True)]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    if location:
        weather_msg = await get_weather(location.latitude, location.longitude)
        await update.message.reply_text(weather_msg)
    else:
        await update.message.reply_text("No location received. Please try again.")

# ---- Main ----
if __name__ == "__main__":
    load_dotenv()  # loads .env file
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))

    print("Bot is running...")
    app.run_polling()
