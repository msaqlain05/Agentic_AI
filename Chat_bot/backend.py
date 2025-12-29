from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
import os
import json
from operator import add
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
  
load_dotenv()



class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]






llm  =  ChatOpenAI()
chekpointer  = MemorySaver()


def chat_node(state:ChatState):
    message = state['messages']
    response = llm.invoke(message)

    return {"messages" : response}

    









graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)


graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer=chekpointer)



# initial_state = {
    
# }





# while True:
#     user_message = input("Type here: ")
#     print("User: ",user_message)
#     if user_message.strip().lower() in ["exit", "quit", "bye", "close"]:
#         break

#     config  = {
#         "configurable" : {"thread_id":thread_id}
#     }

#     response  = chatbot.invoke({"messages": [HumanMessage(content= user_message)]}, config=config)

#     print("AI: ", response["messages"][-1].content)


# chatbot.get_state(config)






