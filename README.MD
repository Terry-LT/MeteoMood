# MeteoMood - Telegram Weather Bot

**MeteoMood** is a Telegram bot that provides **real-time weather information** based on your location and gives **season-aware clothing advice**. It tells you if it’s raining, snowing, hot, cold, or windy — and suggests what to wear, even adding helpful emojis for a fun touch.

---

## Features
- 🌡️ Current temperature at your location  
- 💨 Wind speed and alerts for strong wind  
- 🌧️ Rain and ❄️ snow detection  
- 🧥 Season-aware clothing advice  
- ☂️ Umbrella or boots recommendation  
- 🧢 Cap/hood recommendation for strong wind  
- Automatically adjusts advice depending on **season**  
- Easy-to-use **location sharing** via Telegram  

---

## Usage
1. Start the bot by sending `/start` in Telegram.  
2. Share your location when prompted.  
3. Receive instant weather info and clothing advice.

---

## Installation
1. **Clone this repository**:  
   ```
   git clone https://github.com/yourusername/MeteoMood.git
   cd MeteoMood
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   
Windows:
   ```bash
   venv\Scripts\activate
   ```

Linux / macOS:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a .env file and add your Telegram token:
   ```bash
   TELEGRAM_BOT_TOKEN=YOUR_TOKEN
   ```

6. Run the bot:
   ```bash
   python main.py
   ```