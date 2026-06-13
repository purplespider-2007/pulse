import os
import requests
from datetime import datetime


# -------------------------
# Function 1: Get Weather
# -------------------------
def fetch_weather():
    try:
        city = os.getenv("CITY")
        api = os.getenv("OPENWEATHER_API")

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api}&units=metric"
        )

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()

        return {
            "city": city,
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"]
        }

    except Exception as e:
        return {"error": f"Weather unavailable ({e})"}


# -------------------------
# Function 2: Get Quote
# -------------------------
def fetch_quote():
    try:
        url = "https://zenquotes.io/api/random"

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()[0]

        return {
            "quote": data["q"],
            "author": data["a"]
        }

    except Exception as e:
        return {"error": f"Quote unavailable ({e})"}


# -------------------------
# Function 3: Build Summary
# -------------------------
def build_summary(weather, quote):

    now = datetime.now().strftime("%A, %d %B %Y")

    lines = [
        "",
        f"☀️ Pulse — {now}",
        "-" * 35
    ]

    if "error" in weather:
        lines.append(weather["error"])
    else:
        lines.append(
            f"Weather in {weather['city']}:"
        )
        lines.append(
            f"{weather['temp']}°C • {weather['desc']}"
        )

    lines.append("")

    if "error" in quote:
        lines.append(quote["error"])
    else:
        lines.append(
            f"Quote:\n\"{quote['quote']}\""
        )
        lines.append(f"— {quote['author']}")

    return "\n".join(lines)


# -------------------------
# Function 4: Execute
# -------------------------
def run():
    weather = fetch_weather()
    quote = fetch_quote()

    summary = build_summary(weather, quote)

    print(summary)


if __name__ == "__main__":
    run()