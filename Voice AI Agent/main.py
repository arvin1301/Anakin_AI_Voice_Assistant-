import os
import time
import requests
import wikipedia
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime as dt
import cv2
import urllib.parse  #  for proper Google search encoding
from dotenv import load_dotenv
from openai import OpenAI


# -----------------------------
# 1. Load environment variables
# -----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env file")

# Groq uses an OpenAI-compatible API
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)

# Wikipedia language
wikipedia.set_lang("en")

# -----------------------------
# 2. Text-to-Speech (TTS)
#    with mute/unmute support
# -----------------------------
VOICE_ENABLED = True  # global toggle


def speak(text: str, force: bool = False) -> None:
    """
    Speak text and also print it (blocking).

    VOICE_ENABLED = False will mute all speech unless force=True.
    """
    global VOICE_ENABLED

    if not text:
        return

    print(f"Anakin: {text}")

    # If muted and not forced, just print, don't speak
    if not VOICE_ENABLED and not force:
        return

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS Error: {e}")


# -----------------------------
# 3. Speech-to-Text (STT)
# -----------------------------
recognizer = sr.Recognizer()


def listen() -> str:
    """Listen from microphone and return recognized text (lowercase)."""
    with sr.Microphone() as source:
        print("\nListening...")

        # Better noise handling
        recognizer.adjust_for_ambient_noise(source, duration=1.2)

        # Allow natural pauses in long questions
        recognizer.pause_threshold = 2.0       # YOU CAN PAUSE 2 SECONDS
        recognizer.phrase_threshold = 0.1      # small bursts treated as part of speech
        recognizer.non_speaking_duration = 0.5 # silence allowed before speech starts

        try:
            # timeout = max wait for speech to START
            # phrase_time_limit = max length of your entire question
            audio = recognizer.listen(source, timeout=12, phrase_time_limit=18)
        except sr.WaitTimeoutError:
            print("Listening timed out (no speech).")
            speak("I did not hear anything.")
            return ""

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You: {text}")
        return text.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please speak clearly.")
        return ""

    except sr.RequestError:
        speak("There was a problem with the speech recognition service.")
        return ""

    except Exception as e:
        print("STT Error:", e)
        speak("Something went wrong while listening.")
        return ""


# For assignment-style naming: alias listen() as takeCommand()
def takeCommand() -> str:
    """Assignment-style wrapper around listen()."""
    return listen()


# -----------------------------
# 4. Geocoding helper (city/state fallback)
# -----------------------------
def geocode_with_fallback(location_query: str):
    """
    Try to geocode using the full phrase.
    If no result, fall back to first word and last word.
    """
    base_url = "https://geocoding-api.open-meteo.com/v1/search"

    location_query = location_query.strip()
    candidates = []
    if location_query:
        candidates.append(location_query)

    parts = location_query.split()
    if len(parts) > 1:
        candidates.append(parts[0])       # e.g., "bangalore"
        candidates.append(parts[-1])      # e.g., "karnataka"

    seen = set()
    for cand in candidates:
        cand = cand.strip()
        if not cand or cand in seen:
            continue
        seen.add(cand)

        try:
            url = f"{base_url}?name={cand}&count=1"
            geo_data = requests.get(url, timeout=10).json()
            if "results" in geo_data and len(geo_data["results"]) > 0:
                return geo_data["results"][0]
        except Exception as e:
            print("Geocoding Error:", e)
            continue

    return None


# -----------------------------
# 5. Live Weather (Open-Meteo)
# -----------------------------
def get_live_weather(location_query: str) -> str:
    """
    Fetch live weather using Open-Meteo.
    Supports: state-only, city-only, or "city state".
    """
    try:
        result = geocode_with_fallback(location_query)
        if result is None:
            return f"I could not find {location_query}."

        lat = result["latitude"]
        lon = result["longitude"]
        city = result.get("name")
        state = result.get("admin1")
        country = result.get("country")

        location_full = ", ".join(x for x in [city, state, country] if x)

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        weather_data = requests.get(weather_url, timeout=10).json()

        if "current_weather" not in weather_data:
            return "I could not get the weather right now."

        current = weather_data["current_weather"]
        temp = current["temperature"]
        wind = current["windspeed"]
        direction = current["winddirection"]

        return (
            f"The weather in {location_full} is {temp} degrees Celsius, "
            f"with wind speed {wind} kilometers per hour "
            f"and wind direction {direction} degrees."
        )

    except Exception as e:
        print("Weather Error:", e)
        return "There was an error getting the weather."


# -----------------------------
# 6. Wikipedia
# -----------------------------
def get_wikipedia_summary(topic: str) -> str:
    try:
        return wikipedia.summary(topic, sentences=2)
    except wikipedia.DisambiguationError as e:
        opts = ", ".join(e.options[:3])
        return f"{topic} has multiple results. For example: {opts}. Please be specific."
    except wikipedia.PageError:
        return f"I could not find a page for {topic}."
    except Exception as e:
        print("Wikipedia Error:", e)
        return "I had trouble reaching Wikipedia."


# -----------------------------
# 7. Groq Llama-3.1
# -----------------------------
def ask_groq(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Anakin, a friendly and concise voice assistant. "
                        "Keep answers short, 2–3 sentences maximum."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=80,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print("Groq Error:", e)
        return "I had a problem contacting the Groq server."


# -----------------------------
# 8. Helper: Time & Date
# -----------------------------
def get_time_string() -> str:
    now = dt.datetime.now()
    return now.strftime("%I:%M %p")  # e.g., 03:45 PM


def get_date_string() -> str:
    today = dt.datetime.now()
    return today.strftime("%B %d, %Y")  # e.g., December 05, 2025


# -----------------------------
# 9. Custom Commands: Notes, Reminders, Photos
# -----------------------------
NOTES_FILE = "notes.txt"
REMINDERS_FILE = "reminders.txt"
PHOTOS_DIR = "photos"


def write_note():
    """Ask the user for a note and save it in notes.txt."""
    speak("What should I write in the note?")
    note_text = takeCommand()
    if not note_text:
        speak("I did not catch the note. Please try again later.")
        return

    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {note_text}\n")
        speak("I have written your note.")
    except Exception as e:
        print("Note Error:", e)
        speak("Sorry, I could not save your note.")


def set_reminder():
    """Ask the user for a reminder text and save it in reminders.txt."""
    speak("What should I remind you about?")
    reminder_text = takeCommand()
    if not reminder_text:
        speak("I did not catch the reminder.")
        return

    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(REMINDERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {reminder_text}\n")
        speak("I have saved your reminder.")
    except Exception as e:
        print("Reminder Error:", e)
        speak("Sorry, I could not save your reminder.")


def take_photo():
    """Capture a photo from the default webcam and save it to photos/."""
    try:
        os.makedirs(PHOTOS_DIR, exist_ok=True)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Sorry, I could not access the camera.")
            return

        ret, frame = cap.read()
        cap.release()

        if not ret:
            speak("I could not capture a photo.")
            return

        filename = dt.datetime.now().strftime("photo_%Y%m%d_%H%M%S.png")
        filepath = os.path.join(PHOTOS_DIR, filename)
        cv2.imwrite(filepath, frame)

        speak("I have taken a photo and saved it for you.")
        print(f"Photo saved at: {filepath}")

    except Exception as e:
        print("Camera Error:", e)
        speak("Something went wrong while taking the photo.")


# -----------------------------
# 10. Wish Me (Time-based greeting)
# -----------------------------
def wishMe():
    hour = dt.datetime.now().hour

    if 0 <= hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 18:
        greet = "Good afternoon!"
    else:
        greet = "Good evening!"

    speak(greet)
    speak("How can I help you today?")


# -----------------------------
# 11. Main Assistant Loop (console / PyCharm)
# -----------------------------
def main():
    global VOICE_ENABLED

    # Initial system greeting
    speak(
        "Initializing your voice assistant Anakin.",
        force=True
    )

    # Time-based greeting
    wishMe()

    # Instructions for the user
    speak(
        "You can ask for weather, Wikipedia, time, Google, YouTube, or general questions. "
        "You can also say write a note, set a reminder, or take a photo. "
        "Say stop Anakin to mute my voice, or exit if you want me to stop.",
        force=True,
    )

    while True:
        user_text = takeCommand()
        if not user_text:
            continue

        # Exit commands
        if any(word in user_text for word in ["exit", "quit", "bye"]):
            speak("Goodbye.", force=True)
            break

        # Voice control: mute / unmute
        if "stop anakin" in user_text or "mute anakin" in user_text:
            speak("Okay, I will stop speaking now. I am muted.", force=True)
            VOICE_ENABLED = False
            continue

        if "start anakin" in user_text or "anakin speak" in user_text or "unmute" in user_text:
            VOICE_ENABLED = True
            speak("I am back. I will speak again.", force=True)
            continue

        # Time and date
        if "time" in user_text:
            speak(f"The time is {get_time_string()}.")
            continue

        if "date" in user_text or "today's date" in user_text:
            speak(f"Today is {get_date_string()}.")
            continue

        # Open websites
        if "open google" in user_text:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
            continue

        if "open youtube" in user_text:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
            continue

        if "open stackoverflow" in user_text or "open stack overflow" in user_text:
            speak("Opening Stack Overflow.")
            webbrowser.open("https://stackoverflow.com")
            continue

        #  Google search with proper query
        if "search google for" in user_text or "google" in user_text:
            if "search google for" in user_text:
                query = user_text.split("search google for", 1)[1].strip()
            else:
                parts = user_text.split("google", 1)
                query = parts[1].strip() if len(parts) > 1 else ""

            if not query:
                speak("What should I search on Google?")
                query = takeCommand()

            if query:
                encoded = urllib.parse.quote_plus(query)
                url = f"https://www.google.com/search?q={encoded}"
                speak(f"Searching Google for {query}")
                webbrowser.open(url)
            else:
                speak("I did not get the search term.")
            continue

        # Weather
        if "weather" in user_text:
            location = None
            if " in " in user_text:
                location = user_text.split(" in ", 1)[1].strip()
            if not location:
                speak("Which location? You can say just a city or a state, like Bangalore or Karnataka.")
                location = takeCommand()

            if location:
                speak(get_live_weather(location))
            else:
                speak("I did not catch the location.")
            continue

        # Wikipedia
        if user_text.startswith("wikipedia") or user_text.startswith("wiki "):
            topic = (
                user_text.replace("wikipedia", "", 1)
                .replace("wiki", "", 1)
                .strip()
            )
            if not topic:
                speak("What should I search on Wikipedia?")
                topic = takeCommand()

            if topic:
                speak(get_wikipedia_summary(topic))
            else:
                speak("I did not catch the topic.")
            continue

        # Custom commands: notes, reminders, photos
        if "write a note" in user_text or "take a note" in user_text or "make a note" in user_text:
            write_note()
            continue

        if "set a reminder" in user_text or "remind me" in user_text:
            set_reminder()
            continue

        if "take a photo" in user_text or "take a picture" in user_text or "click a photo" in user_text:
            take_photo()
            continue

        # General Groq AI
        reply = ask_groq(user_text)
        speak(reply)
        time.sleep(0.2)


if __name__ == "__main__":
    main()