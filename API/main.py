from urllib import response
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI()

client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "You are a helpful assistant."},
    ]
)

print(response.choices[0].message.content)
