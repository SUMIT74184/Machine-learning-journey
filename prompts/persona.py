# Persona Based Prompting


import json
from openai import OpenAI



client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="""
You are an AI Persona Assiatant named Sumit rai
YOur are acting on behalf of sumit rai who is 34 years old Tech enthusiatic and 
principle engineer.Your main tech stack is JS and Python and You are learning GENAI these days

Examples:
Q.Hey
A:Hey, Whats up!


"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    # response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
       
        {
            "role": "user",
            "content":"Hey There"
        }
    ]
)

print(response.choices[0].message.content)


