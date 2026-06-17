from dotenv import load_dotenv

load_dotenv()  # MUST be before any core/ imports

from utils.audio_preprocessor import process_input
from core.transcriber import transcribe_all


source = "https://youtu.be/4vfvvzzwcwI?si=cYIL9N8korn-sAYY"
language = "english"


chunks = process_input(source)


transcript = transcribe_all(chunks, language)
print("\n" + "=" * 60)
print("📝 TRANSCRIPT")
print("=" * 60)
print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
