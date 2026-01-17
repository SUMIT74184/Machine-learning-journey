from google import genai

# create client
client = genai.Client(
 api_key="AIzaSyCQnOAqe5BPnSXyrlGGzu36X8_P-ql3p60"
)

# generate text
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in few words"
)

# print result
print(response.text)



