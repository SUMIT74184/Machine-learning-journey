import json
from openai import OpenAI
import requests
from pydantic import BaseModel, Field
from typing import Optional
import os
import speech_recognition as sr

import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer


client = OpenAI(
    api_key=os.getenv("GOOGLE_GEMINI_API"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# - for every tool wait for the observe step which is the output from the called tool.

async_client = AsyncOpenAI(
     api_key=os.getenv("GOOGLE_GEMINI_API"),
)

async def tts(speech:str):
   async with  async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        instructions="Always speak in respectful manner and with full of delight and joy",
        input=speech,
        response_format="pcm"
           
    )as response:
       with LocalAudioPlayer.play(response):
           pass



message_history=[]

def get_weather(city: str):
 
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

def run_command(cmd:str):
    result=os.system(cmd)
    return result

avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""


class MyOutput(BaseModel):
    step:str=Field(..., description="The Id of the step.Example:PLAN,OUTPUT,TOOL ")
    content:Optional[str]=Field(None,description="The optional string content for ")
    tool:Optional[str]=Field(None,description="The Id of the tool to call")
    input:Optional[str]=Field(None,description="The input params for the tool")
    output:Optional[str]=Field(None,description="The output from the tool")
    



messages = [
    { "role": "system", "content": system_prompt }
]

r= sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    r.pause_threshold=2
    


    while True:
        user_query = r.listen(source)
        messages.append({ "role": "user", "content": user_query })

        while True:
            response = client.chat.completions.parse(
                model="gemini-2.5-flash",
                messages=messages,
                response_format=MyOutput
            )
            
            print("Processing Audio.... (STT)")
            stt = r.recognize_google(user_query)
            print(stt)
                
            print("You said",stt)
                

            parsed_output: MyOutput = response.choices[0].message.parsed

            messages.append({ "role": "assistant", "content": json.dumps(parsed_output.model_dump()) })

            if parsed_output.step == "plan":
                print(f"{parsed_output.content}")
                continue
            
            if parsed_output.step == "action":
                tool_name = parsed_output.tool
                tool_input = parsed_output.input

                if avaiable_tools.get(tool_name, False) != False:
                    output = avaiable_tools[tool_name].get("fn")(tool_input)
                    messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                    continue
            
            if parsed_output.step == "output":
                print(f"{parsed_output.content}")
                break
            
            
            
            
            