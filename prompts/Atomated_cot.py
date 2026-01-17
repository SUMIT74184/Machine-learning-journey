#Zero-shot prompting
import json
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCQnOAqe5BPnSXyrlGGzu36X8_P-ql3p60",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="YOu should only and ony answer the cooking related content and anything against it ,say sorry and answer as this content is out of my scope"

message_history=[]
message_history.append({"role":"system","content":SYSTEM_PROMPT})


while True:
    response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type":"json_object"},
    messages=message_history
    )

    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result=json.loads(raw_result)

    if parsed_result.get("step")=="Start":
        print("Thinking",parsed_result.get("content"))
        continue

    elif parsed_result.get("step")=="PLAN":
        print("Here we go",parsed_result.get("content"))
        continue

    if  parsed_result.get("step")=="OUTPUT":
        print("Here is the result ",parsed_result.get("content"))
        break
