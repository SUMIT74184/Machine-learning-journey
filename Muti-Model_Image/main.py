from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


client = OpenAI(
    api_key=os.getenv("GOOGLE_GEMINI_API"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"user",
            "content":[
                {"type":"text","text":"Generate a caption for this image in about 50 words and joke on ISSAC newton with this"},
                {"type":"image_url","image_url":{"url":"https://images.pexels.com/photos/6256066/pexels-photo-6256066.jpeg"}}
            ]
        }
    ]
)

print("Response:",response.choices[0].message.content)