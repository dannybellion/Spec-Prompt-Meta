from pathlib import Path
from models import transcribe_audio

def load_context_files():
    """Load the content of spec prompt files from context directory"""
    context_dir = Path("context")
    files = {
        "examples": context_dir / "spec-prompt-examples.md",
        "template": context_dir / "spec-prompt-template.md"
    }
    
    content = {}
    for name, filepath in files.items():
        if filepath.exists():
            content[name] = filepath.read_text()
        else:
            print(f"Warning: {filepath} not found")
    return content

def main():
    # Transcribe audio files
    print("Transcribing audio files...")
    transcriptions = transcribe_audio()
    for filename, text in transcriptions.items():
        print(f"\nFile: {filename}")
        print(f"Transcription: {text}")
    
    # Load context files
    print("\nLoading context files...")
    context = load_context_files()
    for name, content in context.items():
        print(f"\nContext file: {name}")
        print(f"Length: {len(content)} characters")

if __name__ == "__main__":
    main()
