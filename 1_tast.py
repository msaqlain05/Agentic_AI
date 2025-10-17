from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the model
model = ChatOpenAI()

class LLMState(TypedDict):
    question: str
    answer: str  # Corrected spelling from 'asnwer' to 'answer'

# Define the function to handle the QA
def llm_qa(state: LLMState) -> LLMState:
    question = state['question']
    prompt = f'Answer the following question: {question}'  # Fixed typo 'promt' to 'prompt'
    
    # Call the model to get the answer
    answer = model.invoke(prompt)  # Invoke the model with the correct prompt
    state['answer'] = answer.content  # Corrected 'asnwer' to 'answer'
    
    return state

# Define the graph and add the node
graph = StateGraph(LLMState)
graph.add_node('llm_qa', llm_qa)

# Define the edges between the nodes
graph.add_edge(START, 'llm_qa')  
graph.add_edge('llm_qa', END)

# Compile the workflow (added missing parentheses)
workflow = graph.compile()

# Define the initial state with a question
initial_state = {'question': "What is Langgraph?"}

# Invoke the workflow
output_state = workflow.invoke(initial_state)

# Print the output state with the answer
print(output_state)
