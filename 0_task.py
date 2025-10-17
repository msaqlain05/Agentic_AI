from langgraph.graph import END, START, StateGraph, state
from langgraph.typing import StateT
from typing import TypedDict

class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    bmi_label: str  # Changed to bmi_label instead of category

def calculate_bmi(State: BMIState) -> BMIState:
    weight = State['weight_kg']
    height = State['height_m']
    
    # Correct BMI calculation: height squared
    bmi = weight / (height ** 2)
    
    State['bmi'] = round(bmi, 2)
    return State

def label_bmi(State: BMIState) -> BMIState:
    bmi = State['bmi']
    
    # Classifying BMI based on the value
    if bmi < 18.5:
        State['bmi_label'] = 'Underweight'
    elif 18.5 <= bmi < 24.9:
        State['bmi_label'] = 'Normal weight'
    elif 25 <= bmi < 29.9:
        State['bmi_label'] = 'Overweight'
    else:
        State['bmi_label'] = 'Obesity'
    
    return State

# Define the StateGraph with the BMIState type
graph = StateGraph(BMIState)

# Adding nodes to the graph
graph.add_node('calculate_bmi', calculate_bmi)
graph.add_node('label_bmi', label_bmi)

# Defining the edges between the nodes
graph.add_edge(START, 'calculate_bmi')  
graph.add_edge('calculate_bmi', 'label_bmi')
graph.add_edge('label_bmi', END)

# Compile the workflow
workflow = graph.compile()

# Define the initial state with weight and height
initial_state = {'weight_kg': 80, 'height_m': 1.73}

# Invoke the workflow
output_state = workflow.invoke(initial_state)

# Print the output state with bmi and label
print(output_state)






# from IPython.display import Image
# Image(workflow.get_graph().draw_mermaid_png())