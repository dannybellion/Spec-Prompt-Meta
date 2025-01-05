from pathlib import Path
from models import transcribe_audio
from utils import load_template, load_examples, render_prompt

def main():
    # Transcribe audio files
    print("Transcribing audio files...")
    transcript = transcribe_audio()
    for filename, text in transcript.items():
        print(f"\nFile: {filename}")
        print(f"Transcription: {text}")
    
    # Load context files
    print("\nLoading context files...")
    template = load_template()
    examples = load_examples()
    
    # Render prompt
    rendered_prompt = render_prompt(template, examples, transcript)
    print("\nRendered prompt length:", len(rendered_prompt), "characters")


if __name__ == "__main__":
    main()
