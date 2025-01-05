import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List, BinaryIO

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

def transcribe_audio(audio_file: BinaryIO, model: str = "whisper-1") -> str:
    """Transcribe audio file to text using OpenAI's Whisper model
    
    Args:
        audio_file: An opened audio file (mp3, mp4, mpeg, mpga, m4a, wav, or webm)
        model: The OpenAI model to use (default: whisper-1)
    
    Returns:
        The transcribed text from the audio file
    """
    transcription = client.audio.transcriptions.create(
        model=model,
        file=audio_file
    )
    
    return transcription.text
