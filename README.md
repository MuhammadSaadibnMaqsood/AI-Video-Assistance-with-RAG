# AI Video Assistant with RAG

AI Video Assistant with RAG is a Python project that turns a meeting, lecture, or interview video/audio into structured insights. It can take either a YouTube URL or a local audio/video file, preprocess the media, transcribe it, summarize it, extract key meeting artifacts, and allow question-answering over the transcript using a retrieval-augmented generation (RAG) workflow.

## What this project does

The repository contains a full AI pipeline for working with spoken content:

- Accepts a YouTube URL or local media file as input
- Downloads and converts audio when needed
- Splits audio into manageable chunks
- Transcribes speech with Whisper
- Generates a meeting title and summary with Mistral via LangChain
- Extracts action items, decisions, and open questions
- Builds a local vector store with Chroma and embeddings for RAG-based Q&A

## Project structure

- app.py - Streamlit web app with a polished UI for entering a source and viewing results
- main.py - Command-line entry point for running the pipeline directly
- core/ - Core pipeline modules
  - transcriber.py - Whisper-based transcription
  - summarize.py - LLM-based title and summary generation
  - extractor.py - Extraction of action items, decisions, and questions
  - rag_engine.py - RAG chain and Q&A logic
  - vector_store.py - Chroma vector store setup and retrieval
- utils/audio_preprocessor.py - Audio downloading, conversion, chunking, and preprocessing
- vector_db/ - Persisted Chroma database files
- downloades/ - Downloaded audio files
- Requirements.txt - Python dependencies

## Tech stack

- Audio/video handling: yt-dlp, pydub, FFmpeg
- Speech-to-text: OpenAI Whisper
- LLM orchestration: LangChain, Mistral AI
- Vector search/RAG: Chroma, Hugging Face embeddings
- UI: Streamlit

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- FFmpeg installed and available in your PATH
- A Mistral API key
- Optional: a CUDA-enabled GPU for faster Whisper transcription

## Setup

1. Create and activate a virtual environment

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies

   ```bash
   pip install -r Requirements.txt
   ```

3. Create a .env file in the project root with your credentials:

   ```env
   MISTRAL_API_KEY=your_mistral_api_key
   WHISPER_MODEL=small
   ```

## Running the project

### Option 1: Run the CLI version

```bash
python main.py
```

The script will ask for:

- A YouTube URL or a local file path
- A language preference (english or hinglish)

It will then run the pipeline and provide a transcript, summary, action items, decisions, questions, and a chat-style Q&A experience.

### Option 2: Run the Streamlit UI

```bash
streamlit run app.py
```

The app provides a web interface where you can input a source file or URL and view the generated insights.

## Current implementation notes

The repository contains both a CLI pipeline and a Streamlit frontend. The core modules under core/ implement the main logic for transcription, summarization, extraction, and RAG-based Q&A. The Streamlit app includes a polished interface, but the current execution path in app.py is partially scaffolded and uses placeholder values in the live processing flow. In other words, the project is structured for full end-to-end use, but the UI may need additional wiring to fully connect the core modules to the interface.

## Troubleshooting

- If FFmpeg is missing, install it and ensure it is available on your PATH.
- If Whisper is slow, try a smaller model such as base or tiny in the .env file.
- If the app cannot reach Mistral, verify that your Mistral API key is valid and loaded from .env.
- If Chroma embeddings fail, ensure the required packages from Requirements.txt are installed correctly.

## Summary

This repository is a strong starting point for building an AI-powered meeting assistant or video summarizer with transcription, summarization, structured extraction, and conversational retrieval over the transcript.