import os
from pathlib import Path
from openai import OpenAI
from pydantic import BaseModel
from typing import List, BinaryIO, Dict

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str

def get_chat_response(system: str, user: str, model: str = "gpt-4o") -> str:
    """Get a standard chat response from OpenAI
    
    Args:
        system: The system message providing context/instructions
        user: The user's message/query
        model: The OpenAI model to use (default: gpt-4o)
    
    Returns:
        The model's response text
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    
    return completion.choices[0].message.content

def get_structured_response(system: str, user: str, response_model: BaseModel, model: str = "gpt-4o") -> BaseModel:
    """Get a structured response from OpenAI that conforms to a Pydantic model
    
    Args:
        system: The system message providing context/instructions
        user: The user's message/query
        response_model: The Pydantic model class defining the response structure
        model: The OpenAI model to use (default: gpt-4o)
    
    Returns:
        A parsed response matching the provided Pydantic model
    """
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        response_format=response_model
    )
    
    return completion.choices[0].message.parsed

def transcribe_audio(audio_dir: str = "inputs/audio", model: str = "whisper-1") -> Dict[str, str]:
    """Transcribe all audio files in the specified directory using OpenAI's Whisper model
    
    Args:
        audio_dir: Directory containing audio files (default: "inputs/audio")
        model: The OpenAI model to use (default: whisper-1)
    
    Returns:
        Dictionary mapping filenames to their transcribed text
    """
    audio_path = Path(audio_dir)
    if not audio_path.exists():
        raise FileNotFoundError(f"Directory {audio_dir} not found")
        
    supported_formats = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}
    transcriptions = {}
    
    for file_path in audio_path.iterdir():
        if file_path.suffix.lower() in supported_formats:
            with open(file_path, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    model=model,
                    file=audio_file
                )
                transcriptions[file_path.name] = transcription.text
    
    return transcriptions
