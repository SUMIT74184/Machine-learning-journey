from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.mongodb import MongoDBSaver


from pathlib import Path
import os
# import langchain_google_genai

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)


assert os.getenv("GOOGLE_GEMINI_API"), "GOOGLE_GEMINI_API not loaded"

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


# Initializing the state in graph_builder variable
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)



# adding the edges
# START -> chatbot -> END


graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)


graph=graph_builder.compile()

# Compile graph with checkpointer
def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:       
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config = {
            "configurable":{
                "thread_id":1
            }
        }

    updated_state=graph_with_checkpointer.invoke(State({"messages":["hi what is my name can you tell me?"]}),
                                                    config,
                                                    )
    print("\n\n",updated_state)
    
    
    # for chunk in graph_with_checkpointer.stream(
    #     State({"messages":["hi what is my name can you tell me?"]}),
    #     config,
    #     stream_mode="values"
    # ):
        
    #     chunk["messages"][-1].pretty_print()
    
    

# Checkpointer (1) = hi my name is Timios
# we can also stream it instead of invoking .....checkout the documentations
# we can also setup diff thread id for diff data






