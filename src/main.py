from pathlib import Path
from .models import transcribe_audio, get_chat_response, load_text_files
from .utils import load_template, load_examples, render_prompt
import os

def main():
    # Transcribe audio files
    print("Transcribing audio files...")
    transcript = transcribe_audio()
    for filename, text in transcript.items():
        print(f"\nFile: {filename}")
        print(f"Transcription: {text}")
    
    # Load text files
    print("\nLoading text files...")
    text_files = load_text_files()
    if text_files:
        for filename, content in text_files.items():
            print(f"\nLoaded text file: {filename}")
    else:
        print("No text files found in inputs/text/")
    
    # Load context files
    print("\nLoading context files...")
    template = load_template()
    examples = load_examples()
    
    # Render prompt
    rendered_prompt = render_prompt(template, examples, transcript)
    print("\nRendered prompt length:", len(rendered_prompt), "characters")

    # Get chat response and save to file
    system_message = "You are a helpful assistant that processes audio transcripts."
    response = get_chat_response(system_message, rendered_prompt)
    
    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save response to file
    output_file = output_dir / "project-spec.md"
    output_file.write_text(response)
    print(f"\nProject specification saved to: {output_file}")


if __name__ == "__main__":
    main()
