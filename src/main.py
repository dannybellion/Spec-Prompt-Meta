from pathlib import Path
from models import transcribe_audio, get_chat_response
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

    # Get chat response
    system_message = "You are a helpful assistant that processes audio transcripts."
    response = get_chat_response(system_message, rendered_prompt)
    print("\nAI Response:", response)


if __name__ == "__main__":
    main()
