from pathlib import Path
from models import transcribe_audio
from utils import load_template, load_examples

def main():
    # Transcribe audio files
    print("Transcribing audio files...")
    transcriptions = transcribe_audio()
    for filename, text in transcriptions.items():
        print(f"\nFile: {filename}")
        print(f"Transcription: {text}")
    
    # Load context files
    print("\nLoading context files...")
    template = load_template()
    examples = load_examples()


if __name__ == "__main__":
    main()
