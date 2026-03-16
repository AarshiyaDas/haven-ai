# Haven — AI Crisis Companion

Haven is a real-time AI mental health companion that helps users through moments of stress and anxiety using multimodal interaction and proactive schedule-aware check-ins.

![Haven UI](https://img.shields.io/badge/AI-Llama%203.3%2070B-blue) ![Python](https://img.shields.io/badge/Python-3.12-green) ![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey) ![Cloud](https://img.shields.io/badge/Hosted-Google%20Cloud-orange)

## Features

- Real-time streaming responses using Server-Sent Events — words appear live as the AI thinks
- Schedule-aware proactive alerts — paste your schedule and Haven checks in 30 minutes before stressful events
- Camera-enabled environment grounding — personalises the 5-4-3-2-1 grounding technique to your surroundings
- Voice input and text-to-speech — fully hands-free conversation
- Therapist session report — generates a structured clinical summary after each session
- Responsible AI design — never diagnoses, always encourages professional help

## Tech Stack

- Backend: Python, Flask, Server-Sent Events
- AI Model: Llama 3.3 70B via Hugging Face Inference API (Groq provider)
- Frontend: HTML, CSS, JavaScript (vanilla)
- Infrastructure: Google Cloud Shell
- APIs: Hugging Face Inference API, Web Speech API, MediaDevices Camera API

## How to Run

1. Clone the repo
   git clone https://github.com/AarshiyaDas/haven-ai.git
   cd haven-ai

2. Install dependencies
   pip install flask python-dotenv huggingface_hub

3. Create a .env file
   HF_TOKEN=your_hugging_face_token_here

4. Run the app
   python app.py

5. Open your browser
   http://localhost:8080

## How it Works

Haven uses Llama 3.3 70B through Hugging Face's inference API with Groq as the provider for fast responses. The backend streams tokens to the frontend using Server-Sent Events, creating a real-time typing effect. The schedule parser checks time deltas every minute and fires proactive check-ins 30 minutes before stressful events. After each session, a separate API call generates a structured therapist report summarising emotional arc, triggers, and recommended next steps.

## Architecture

User (browser)
    ↓ voice / text / camera frame
Flask backend (app.py)
    ↓ chat history + system prompt
Hugging Face Inference API → Groq → Llama 3.3 70B
    ↓ streaming tokens (SSE)
Frontend (index.html)
    ↓ text-to-speech
User hears Haven's response

## Why I Built This

Mental health crises don't announce themselves. Most AI tools wait for you to reach out — Haven reaches out first, using your own schedule to know when you might need support. Built in one night as a learning project exploring real-time AI streaming, multimodal web APIs, and responsible AI design.
