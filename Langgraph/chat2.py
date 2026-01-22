from dotenv import load_dotenv
load_dotenv()
from typing_extensions import TypedDict
from typing import Optional,Literal
import os
from openai import OpenAI
from langgraph.graph import StateGraph,START,END


client = OpenAI(
    api_key=os.environ["GOOGLE_GEMINI_API"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class State(TypedDict):
    user_query:str
    llm_output:Optional[str]   
    is_good: Optional[bool]
    
def chatbot(state:State):
    print("Chatbot Node",state)
    response=client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )
    
    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state:State)->Literal["chatbot_gemini","endnode"]:
    print("evaluate_response Node",state)
    if False:
      return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state:State):
    print("chatbot_gemini Node",state)
    response=client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )
    
    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state:State):
    print("endnode",state) 
    return state

    
graph_builder=StateGraph(State)

# Defining the nodes

graph_builder.add_node("chatbot",chatbot)
# graph_builder.add_node("evaluate_response",evaluate_response)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)



# Defining the edges
graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_gemini","endnode")
graph_builder.add_edge("endnode",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"user_query":"Hey, what is the capital of Nagaland in india?"}))

print(updated_state)












