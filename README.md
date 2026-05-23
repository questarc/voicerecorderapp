# 🎙️ Streamlit Voice Recorder

A production-grade browser-based voice recorder built with Streamlit.

## Features

- Record audio directly from the browser microphone
- Visual recording button with status colors
- Playback preview of the captured audio
- Download recording as a WAV file
- Configurable filename prefix and timestamp
- Clean, deployable Streamlit app

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
