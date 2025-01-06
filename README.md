# AI Project Specification Generator

A tool that generates detailed project specification prompts designed to be used by AI coding assistants.

## Features

- 🎤 **Audio Transcription**: Automatically transcribes audio files using OpenAI's Whisper model
- 📝 **Context Integration**: Combines transcripts with template and example files
- 🤖 **AI-Powered**: Uses GPT-4o to generate structured project specifications

## Details

The emergence of AI coding assistants has fundamentally transformed software development. While these powerful tools can generate complex code with remarkable 
speed and accuracy, the true art lies in crafting precise, nuanced prompts. The challenge isn't just about generating code, but articulating requirements with clarity, context, and strategic detail.

This project automates the process of generating comprehensive project specifications by leveraging AI's ability to distill and articulate complex requirements. Instead of manually crafting detailed prompts, we use AI to transform raw inputs like audio transcripts, text notes, and README files into precise, actionable project specifications. By removing human bias and leveraging AI's analytical capabilities, we shift the prompt engineering burden directly to the AI, enabling more efficient and objective project scoping.


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
uv sync
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

1. Place audio files in the `inputs/audio/` directory (supported formats: mp3, mp4, m4a, wav, webm)
2. Place any text files (.md, .txt) in the `inputs/text/` directory for additional context
3. Please the current README.md file in the `inputs/readme/` directory for additional context
3. Run the main script:
```bash
python -m src.main
```

The script will:
1. Transcribe all audio files in the audio directory
2. Load and combine context files
3. Generate a project specification using GPT-4o
4. Save the result to `output/project-spec.md`
