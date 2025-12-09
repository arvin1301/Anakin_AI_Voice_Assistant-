# Anakin_AI_Voice_Assistant-

# 🎤 Anakin – Real-Time AI Voice Assistant

Anakin is a **real-time AI voice assistant** built using:

-  **Groq Llama-3.1-8B-instant** (via OpenAI-compatible API)  
-  **SpeechRecognition** (Google Web Speech API) for Speech-to-Text  
-  **pyttsx3** for offline Text-to-Speech  
-  **Open-Meteo API** for live weather  
-  **Wikipedia API** for knowledge lookup  
-  **Google search** integration  
-  Voice-driven **notes** and **reminders**  
-  **OpenCV** for webcam photo capture  
-  **Streamlit** for a browser-based UI  

This project was developed as a **Data Science internship project at Inlighn Tech** by **Arvind Sharma**.

---

##  Features

-  **Continuous voice listening** (console + Streamlit)
-  **Speech-to-Text (STT)** using `speech_recognition` + Google STT  
-  **Text-to-Speech (TTS)** with `pyttsx3`  
  - Global **mute/unmute** control (`VOICE_ENABLED`)  
-  **Groq Llama-3.1-8B-instant** for general Q&A and chat
-  **Weather queries** using Open-Meteo  
  - Robust **geocoding with fallback** (handles “Bangalore”, “Karnataka”, “Bangalore Karnataka”)  
-  **Wikipedia summaries** – Short 2-sentence topic explanations  
-  **Google Search integration**  
  - Commands like `search google for ...` or `google <query>` open a browser  
-  **Notes** – “write a note”, stored in `notes.txt` with timestamps  
-  **Reminders** – “set a reminder”, stored in `reminders.txt` with timestamps  
-  **Photo capture** – “take a photo” saves webcam images in `photos/`  
-  **Time & Date** queries  
-  **Streamlit UI** for:
  - Start/Stop Listening  
  - Conversation history  

---

##  Tech Stack

- **Language:** Python 3.10+
- **Core Libraries:**
  - `speechrecognition`
  - `pyttsx3`
  - `pyaudio`
  - `requests`
  - `wikipedia`
  - `python-dotenv`
  - `openai` (Groq-compatible client)
  - `opencv-python`
  - `streamlit`
- **External APIs:**
  - [Groq API](https://groq.com) – Llama-3.1-8B-instant  
  - [Open-Meteo](https://open-meteo.com/) – Weather & Geocoding  
  - [Wikipedia](https://pypi.org/project/wikipedia/) – Summaries  
  - Google Search (via `webbrowser` module)

---

##  Project Structure

```bash
anakin-voice-assistant/
├─ main.py                  # Core console-based voice assistant
├─ app.py                   # Streamlit web UI (continuous listening)
├─ requirements.txt         # Python dependencies
├─ .env.example             # Example environment variables
├─ README.md                # Project documentation
├─ LICENSE                  # License (MIT suggested)
├─ docs/
│  └─ Anakin_Voice_Assistant_Research_Documentation.pdf
├─ photos/                  # Auto-created: saved webcam photos
├─ notes.txt                # Auto-created: text notes
├─ reminders.txt            # Auto-created: reminders
└─ .gitignore               # Ignore venv, __pycache__, etc.
⚙️ Installation
1️⃣ Clone the repository
bash
Copy code
git clone https://github.com/<your-username>/anakin-voice-assistant.git
cd anakin-voice-assistant
2️⃣ Create & activate a virtual environment (recommended)
Windows (PowerShell):

bash
Copy code
python -m venv venv
venv\Scripts\activate
Linux / macOS:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure environment variables
Create a .env file in the project root (next to main.py) based on .env.example:

env
Copy code
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
Get your Groq API key from your Groq account.

The default model in this project is llama-3.1-8b-instant.

▶️ Usage
You can run Anakin in two modes:

A. Console Mode (Terminal / PyCharm)
bash
Copy code
python main.py
Workflow:

Anakin introduces itself.

You’ll see messages like:

Listening...

Recognizing...

Speak commands like:

“What is the weather in Bangalore?”

“Wikipedia machine learning”

“Search Google for YOLOv10 tutorials”

“Write a note. I have a meeting tomorrow at 5 PM.”

“Set a reminder. Call mentor at 8 PM.”

“Take a photo”

“Explain overfitting in simple terms”

Say exit, quit, or bye to stop Anakin.

Voice control:

Say “stop Anakin” or “mute Anakin” → TTS is muted (text only).

Say “start Anakin”, “Anakin speak”, or “unmute” → TTS is enabled again.

B. Web UI Mode (Streamlit)
bash
Copy code
streamlit run app.py
This will:

Open a browser tab (usually at http://localhost:8501)

Show:

 Anakin Voice Assistant – Continuous Listening

Buttons:

 Start Listening

 Stop Listening

Conversation history

How it works:

Click Start Listening

Speak your commands (same as console mode)

The assistant will:

Transcribe your speech

Process the command

Speak and display the response

Click Stop Listening or say exit / quit / bye to stop.

 Supported Voice Commands
Some example phrases you can use:

🔹 Time & Date
“What is the time?”

“What is today’s date?”

“Tell me the date today”

🔹 Weather
“What is the weather in Bangalore?”

“Tell me the weather in Karnataka”

“Weather in New Delhi”

🔹 Wikipedia
“Wikipedia machine learning”

“Wiki neural networks”

“Wikipedia Elon Musk”

🔹 Google Search
“Search Google for object detection using YOLOv10”

“Google latest AI news”

“Google Python decorators”

🔹 Notes & Reminders
“Write a note. I have a project review tomorrow.”

“Take a note. Buy groceries today.”

“Set a reminder. Call my friend at 6 PM.”

“Remind me to submit my assignment.”

🔹 Camera
“Take a photo”

“Click a photo”

“Take a picture”

🔹 General Questions (LLM)
“Explain overfitting in simple terms.”

“What is the difference between supervised and unsupervised learning?”

“Help me understand gradient descent.”

 Architecture Overview
Pipeline (high-level):

text
Copy code
User Speech
     ↓
SpeechRecognition (Google STT)
     ↓
Recognized Text (lowercased)
     ↓
Intent Recognition / Command Engine
     ↓
 ┌───────────────────────────────┬──────────────────────────────┐
 | Predefined Commands           |   General Query (fallback)   |
 | (weather, wiki, google, etc.) | → Groq Llama-3.1-8B-instant  |
 └───────────────────────────────┴──────────────────────────────┘
     ↓
Action or AI Response
     ↓
Text-to-Speech (pyttsx3) + UI Output (Streamlit / Console)
 Research Documentation
Full research-style project report is available in:

bash
Copy code
docs/Anakin_Voice_Assistant_Research_Documentation.pdf
It includes:

Problem statement

Objectives

Literature review

System design & architecture

Algorithms (STT, TTS, intent recognition, weather, LLM)

Implementation details

Testing & results

Limitations and future work

 Testing
Tested with:

Windows 10

Python 3.10

Conda/venv virtual environments

Typical laptop mic & webcam

Manual test cases include:

Time/date queries

Weather queries (city and state-based)

Wikipedia lookups

Google search commands

Note & reminder creation

Photo capture

General LLM Q&A

Exit, mute, and unmute commands

🛡 License
This project is licensed under the MIT License – see the LICENSE file for details.

 Contributing
Contributions are welcome!

Ideas to improve:

Add wake-word detection (“Hey Anakin”)

Add offline STT (Whisper, Vosk)

Add multi-language support

Save conversation history to a database

Add more tools/APIs (YouTube transcripts, WikiHow, Serper, etc.)

Steps:

Fork the repo

Create a new branch: feature/my-awesome-feature

Commit your changes

Push to the branch

Open a Pull Request 

 Author
Arvind Sharma
Data Science Intern – Inlighn Tech

Focus areas: Computer Vision, NLP, LLMs, Time Series

Tools: YOLOv10, DeepSORT, PaddleOCR, Llama, Gemini, Streamlit, Flask

If you use this project or find it helpful, feel free to  the repo and mention it in your portfolio!

yaml
Copy code

---

## 3. `.env.example`

```env
# Copy this file to `.env` and fill your credentials

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
4. LICENSE (MIT)
text
Copy code
MIT License

Copyright (c) 2025 Arvind Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN  
THE SOFTWARE.
5. .gitignore
gitignore
Copy code
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.log

# Virtual env
venv/
.env

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Photos & runtime files (optional - or keep them tracked if you want)
photos/
notes.txt
reminders.txt
