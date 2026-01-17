#Zero-shot prompting

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCQnOAqe5BPnSXyrlGGzu36X8_P-ql3p60",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="YOu should only and ony answer the cooking related content and anything against it ,say sorry and answer as this content is out of my scope"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
       
        {
            "role": "user",
            "content":"explain me gauss theorem ?"
        }
    ]
)

print(response.choices[0].message)