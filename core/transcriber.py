import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        print(f"Loading whisper model ({WHISPER_MODEL}) this may take a while")
        _model = whisper.load_model(WHISPER_MODEL)

        print("Whisper model loaded successfully!")

    return _model


def transcribe_chunk(chunks_path: str, translate: bool = False) -> str:
    model = load_model()

    task = "translate" if translate else "transcribe"
    print(f"Transcribing chunk ({task} {WHISPER_MODEL})...")

    result = model.transcribe(chunks_path)

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
