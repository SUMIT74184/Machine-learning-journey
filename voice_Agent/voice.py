import speech_recognition as sr
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

#Chained Architecture from speech to text -> speech

client = OpenAI(
    api_key="sk-",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async_client = AsyncOpenAI(
    api_key="sk-",
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
       
SYSTEM_PROMPT=f"""
                Yor're an expert voice agent. YOu are given the transcript of what 
                user has said using voice.
                You need to output as if you are an voice agent and whatever you speak
                will be converted back to audio using AI and played back to user
            """           


def main():
    r = sr.Recognizer() # Speech to text
    
    with sr.Microphone() as source: #Mic Access
         r.adjust_for_ambient_noise(source)   
         r.pause_threshold=2
        
        
         
         while(True):
         
            print("Speak Something....")
            audio = r.listen(source) 
            
            print("Processing Audio.... (STT)")
            stt = r.recognize_google(audio)
            print(stt)
            
            print("You said",stt)
            
          
            
            messages=[ {"role":"system","content":SYSTEM_PROMPT}]
            
            messages.append({"role":"user","content":stt})
            
            response=client.chat.completions.create(
                model="chatgpt-4o-latest",
                messages=messages
            )
            print("AI Response",response.choices[0].message.content)
            asyncio.run(tts(speech=response.choices[0].message.content))
         
            

main()
    
    
    
    
    
    
    