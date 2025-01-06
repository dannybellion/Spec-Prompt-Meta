# AI Project Specification Generator

A tool that generates detailed project specification prompts designed to be used by AI coding assistants.

## Features

- 🎤 **Audio Transcription**: Automatically transcribes audio files using OpenAI's Whisper model
- 📝 **Context Integration**: Combines transcripts with template and example files
- 🤖 **AI-Powered**: Uses GPT-4o to generate structured project specifications

## Project Structure

The project is organized as follows:

- 📁 **src/**: Core source code
  - `main.py`: Main application entry point
  - `models.py`: OpenAI API integration and data models
  - `utils.py`: Utility functions for file handling and template rendering
  - `prompt.j2`: Jinja2 template for prompt generation

## Setup

1. Install dependencies using uv:
```bash
uv pip install openai pydantic jinja2
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

1. Place audio files in the `inputs/audio/` directory (supported formats: mp3, mp4, m4a, wav, webm)
2. Place any text files (.md, .txt) in the `inputs/text/` directory for additional context
3. Add context files in the `context/` directory:
   - `spec-prompt-template.md`: Template for specification generation
   - `spec-prompt-examples.md`: Example specifications
3. Run the main script:
```bash
python -m src.main
```

The script will:
1. Transcribe all audio files in the audio directory
2. Load and combine context files
3. Generate a project specification using GPT-4
4. Save the result to `output/project-spec.md`

## Repository Map Generation

The project includes a tool to generate a visual representation of the repository structure:

```bash
python src/repo_map.py
```

This will create a markdown file at `output/repo_map.md` showing the project's directory structure.

## Dependencies

- OpenAI
- Pydantic
- Jinja2

## License

MIT License
