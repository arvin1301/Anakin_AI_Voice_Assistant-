import time
import urllib.parse
import webbrowser

import streamlit as st

from main import (
    takeCommand,
    speak,
    get_time_string,
    get_date_string,
    get_live_weather,
    get_wikipedia_summary,
    ask_groq,
    write_note,
    set_reminder,
    take_photo,
)

# -----------------------------
# Command handler for Streamlit
# -----------------------------
def process_command(user_text: str) -> str:
    user_text = user_text.lower().strip()

    # Exit / quit / bye → stop listening in Streamlit
    if any(word in user_text for word in ["exit", "quit", "bye"]):
        reply = "Goodbye. Stopping listening now."
        speak(reply)
        st.session_state.listening = False
        return reply

    # Time & Date
    if "time" in user_text:
        reply = f"The time is {get_time_string()}."
        speak(reply)
        return reply

    if "date" in user_text or "today's date" in user_text:
        reply = f"Today is {get_date_string()}."
        speak(reply)
        return reply

    # Open websites
    if "open google" in user_text:
        reply = "Opening Google."
        speak(reply)
        webbrowser.open("https://www.google.com")
        return reply

    if "open youtube" in user_text:
        reply = "Opening YouTube."
        speak(reply)
        webbrowser.open("https://www.youtube.com")
        return reply

    if "open stackoverflow" in user_text or "open stack overflow" in user_text:
        reply = "Opening Stack Overflow."
        speak(reply)
        webbrowser.open("https://stackoverflow.com")
        return reply

    # Google search
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
            reply = f"Searching Google for {query}."
            speak(reply)
            webbrowser.open(url)
        else:
            reply = "I did not get any search term."
            speak(reply)

        return reply

    # Weather
    if "weather" in user_text:
        location = None
        if " in " in user_text:
            location = user_text.split(" in ", 1)[1].strip()
        if not location:
            speak("Which location? You can say just a city or a state, like Bangalore or Karnataka.")
            location = takeCommand()

        if location:
            reply = get_live_weather(location)
        else:
            reply = "I did not catch the location."

        speak(reply)
        return reply

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
            reply = get_wikipedia_summary(topic)
        else:
            reply = "I did not catch the topic."

        speak(reply)
        return reply

    # Custom commands: notes, reminders, photos
    if "write a note" in user_text or "take a note" in user_text or "make a note" in user_text:
        write_note()
        reply = "I have written your note."
        return reply

    if "set a reminder" in user_text or "remind me" in user_text:
        set_reminder()
        reply = "I have saved your reminder."
        return reply

    if "take a photo" in user_text or "click a photo" in user_text or "take a picture" in user_text:
        take_photo()
        reply = "I have taken a photo using your camera."
        return reply

    # Fallback: General AI
    reply = ask_groq(user_text)
    speak(reply)
    return reply


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Anakin Voice Assistant", page_icon="🎤")

st.title("🎤 Anakin Voice Assistant – Continuous Listening")

st.write(
    """
- Press **Start Listening** to let Anakin listen in a loop  
- Say **exit / quit / bye** or press **Stop Listening** to stop  
"""
)

# Session state
if "listening" not in st.session_state:
    st.session_state.listening = False

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns(2)
with col1:
    if st.button(" Start Listening"):
        st.session_state.listening = True
        st.success("Listening started… Speak now!")

with col2:
    if st.button(" Stop Listening"):
        st.session_state.listening = False
        st.warning("Listening stopped.")

placeholder = st.empty()

# Continuous listening loop
if st.session_state.listening:
    while st.session_state.listening:
        placeholder.info("🎙️ Listening... Speak now")

        user_text = takeCommand()

        if user_text:
            st.session_state.history.append(("You", user_text))
            with st.spinner("Processing…"):
                bot_reply = process_command(user_text)
            st.session_state.history.append(("Anakin", bot_reply))

        # If process_command turned off listening (exit), break
        if not st.session_state.listening:
            break

        # Show history
        history_md = ""
        for speaker, msg in st.session_state.history[::-1]:
            history_md += f"**{speaker}:** {msg}\n\n"
        st.markdown(history_md)

        time.sleep(0.5)

# Show history even when not listening
st.subheader("Conversation History")
history_md = ""
for speaker, msg in st.session_state.history[::-1]:
    history_md += f"**{speaker}:** {msg}\n\n"
st.markdown(history_md)