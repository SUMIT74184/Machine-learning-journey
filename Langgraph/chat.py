from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

from langchain_google_genai import ChatGoogleGenerativeAI


from pathlib import Path
import os
# import langchain_google_genai

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)


assert os.getenv("GOOGLE_GEMINI_API"), "GOOGLE_GEMINI_API not loaded"

# llm = init_chat_model(
#     model="gemini-2.5-flash",
#     model_provider="google_genai"
# )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_GEMINI_API")
)

# Defining the State with list and appending the message via add_messages
class State(TypedDict):
    messages:Annotated[list,add_messages]

# defining the Node
def chatbot(state:State):
    # print("\n\nInside chatbot node",state) Instead of this
    response = llm.invoke(state.get("messages"))
    # return {"messages":["Hi,This is a message from ChatBot Node"]}
    return {"messages": [response]}

def samplenode(state:State):
    print("\n\nInside sample node",state)
    return {"messages":["Sample message Appended"]}
    
    


# Initializing the state in graph_builder variable
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)


# adding the edges
# START -> chatbot -> samplenode -> END


graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["hii my name is timios"]}))
print("\n\n",updated_state)









