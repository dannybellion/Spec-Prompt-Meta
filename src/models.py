from openai import OpenAI
from pydantic import BaseModel
from typing import List

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str

def get_chat_response(prompt: str) -> str:
    """Get a standard chat response from OpenAI"""
    client = OpenAI()
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content

def get_structured_math_response(problem: str) -> MathResponse:
    """Get a structured math solution response from OpenAI"""
    client = OpenAI()
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful math tutor. Guide the user through the solution step by step."
            },
            {
                "role": "user",
                "content": problem
            }
        ],
        response_format=MathResponse
    )
    
    return completion.choices[0].message.parsed
