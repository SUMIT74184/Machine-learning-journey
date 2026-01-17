from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCQnOAqe5BPnSXyrlGGzu36X8_P-ql3p60",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":"Your are an expert in cooking and explain how to cook indian food"},
       
        {
            "role": "user",
            "content":"How to cook sahi paneer ?"
        }
    ]
)

print(response.choices[0].message)


