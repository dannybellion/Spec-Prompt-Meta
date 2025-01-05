from pathlib import Path
from jinja2 import Template
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
    
    # Load and render Jinja template
    with open('src/prompt.j2') as f:
        template_content = f.read()
    
    jinja_template = Template(template_content)
    rendered_prompt = jinja_template.render(
        template=template,
        examples=examples
    )
    
    print("\nRendered prompt length:", len(rendered_prompt), "characters")


if __name__ == "__main__":
    main()
