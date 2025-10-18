from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Any

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Ensure the OpenAI API key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is missing!")

# Initialize the OpenAI model
model = ChatOpenAI(api_key=OPENAI_API_KEY)

class BlogState(TypedDict):
    title: str
    outline: str
    content: str
    evaluate: int

def create_outline(state: BlogState) -> BlogState:
    """
    Generate an outline for the blog based on the title provided in the state.
    """
    title = state['title']
    prompt = f"Generate an outline for a blog on the topic - {title}"

    # Ensure the model is used correctly by invoking the prompt
    outline_response = model.invoke(prompt)
    outline = outline_response.content  # Assuming 'content' holds the text returned

    state['outline'] = outline

    return state

def create_blog(state: BlogState) -> BlogState:
    """
    Generate a detailed blog based on the provided title and outline in the state.
    """
    title = state['title']
    outline = state['outline']

    prompt = f"Write a detailed blog on the title '{title}' using the following outline:\n{outline}"

    # Get the generated content for the blog
    content_response = model.invoke(prompt)
    content = content_response.content  # Assuming 'content' contains the blog text

    state['content'] = content

    return state

def evaluate_blog(state: BlogState) -> BlogState:
    """
    Evaluate the generated blog content on a scale of 1 to 10 based on the context.
    """
    content = state['content']

    prompt = f"Evaluate my blog based on the following content:\n{content}\nProvide an integer rating between 1 and 10."
    
    
    try:
        # Ensure the evaluation is parsed correctly as an integer
        evaluation_response = model.invoke(prompt)
        evaluation = int(evaluation_response.content)  # Get integer from response content
    except ValueError:
        evaluation = 0  # Default value if the response is invalid or can't be parsed
    
    state['evaluate'] = evaluation

    return state

# Define the state graph for the workflow
graph = StateGraph(BlogState)

# Add nodes for each of the steps in the blog creation process
graph.add_node("create_outline", create_outline)
graph.add_node("create_blog", create_blog)
graph.add_node("evaluate_blog", evaluate_blog)

# Add edges to define the flow of the process
graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', 'evaluate_blog')
graph.add_edge('evaluate_blog', END)

# Compile the workflow
workflow = graph.compile()

# Define the initial state with title as input
initial_state = {'title': "how to install python?"}

# Invoke the workflow and get the output state
output_state = workflow.invoke(initial_state)

# Print the output state with the blog content and evaluation
print("Blog Title:", output_state['title'])
print("Blog Content:", output_state['content'])
print('------------------------------------------')
print("Evaluation Rating:", output_state['evaluate'])
