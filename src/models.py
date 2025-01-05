import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str

def get_chat_response(system_msg: str, user_msg: str, model: str = "gpt-4o") -> str:
    """Get a standard chat response from OpenAI
    
    Args:
        system_msg: The system message providing context/instructions
        user_msg: The user's message/query
        model: The OpenAI model to use (default: gpt-4o)
    
    Returns:
        The model's response text
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )
    
    return completion.choices[0].message.content

def get_structured_response(system_msg: str, user_msg: str, response_model: BaseModel, model: str = "gpt-4o") -> BaseModel:
    """Get a structured response from OpenAI that conforms to a Pydantic model
    
    Args:
        system_msg: The system message providing context/instructions
        user_msg: The user's message/query
        response_model: The Pydantic model class defining the response structure
        model: The OpenAI model to use (default: gpt-4o)
    
    Returns:
        A parsed response matching the provided Pydantic model
    """
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        response_format=response_model
    )
    
    return completion.choices[0].message.parsed
