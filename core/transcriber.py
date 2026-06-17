import whisper
import os
import torch

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading whisper model ({WHISPER_MODEL}) on {device.upper()}... this may take a while")
        if device == "cpu":
            print("⚠️ CUDA GPU not detected. Running on CPU will be slower.")
            print("💡 TIP: You can change WHISPER_MODEL in your .env file to 'base' or 'tiny' for faster performance on CPU.")
        _model = whisper.load_model(WHISPER_MODEL, device=device)
        print("Whisper model loaded successfully!")

    return _model


def transcribe_chunk(chunks_path: str, translate: bool = False) -> str:
    model = load_model()

    task = "translate" if translate else "transcribe"
    print(f"Transcribing chunk ({task} {WHISPER_MODEL})...")

    # Explicitly set fp16=False on CPU to avoid warnings and speed up transcription
    use_fp16 = torch.cuda.is_available()
    result = model.transcribe(chunks_path, fp16=use_fp16)

    return result["text"]


def transcribe_all(chunks: list, translate: bool = False) -> str:
    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1}/{len(chunks)} ---")

        text = transcribe_chunk(chunk, translate)
        full_transcript += text + "\n"

        if os.path.exists(chunk):
            os.remove(chunk)
            print(f"Deleted chunk {chunk}")

    print("Transcription complete")
    return full_transcript
