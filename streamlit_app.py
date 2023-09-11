import streamlit as st
from api_setup import setup_api_key
from conversation_simulation import simulate_conversation, generate_prompts, generate_responses, evaluate_responses

def generate_next_message(previous_response):
    return "YOUR_LOGIC_HERE_BASED_ON_previous_response"

st.title("GPT-4 Prompt Optimizer")

task = st.text_area("Enter your task:", "Write a summary of the solar system")
num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=4)
previous_solutions = []

if st.button("Generate Optimized Prompt"):
    # Perform one iteration only
    N = 1
    
    # Stage 1: Generate Prompts
    with st.spinner('Stage 1: Generating Prompts...'):
        generated_prompts = generate_prompts(task, num_prompts)
    st.write("Generated Prompts:", generated_prompts)

    # Stage 2: Generate Responses
    with st.spinner('Stage 2: Generating Responses...'):
        generated_responses = generate_responses(generated_prompts, task)
    st.write("Generated Responses:", generated_responses)
        
    # Stage 3: Evaluate Responses
    with st.spinner('Stage 3: Evaluating Responses...'):
        evaluation = evaluate_responses(generated_responses, task)
    st.write("Evaluation:", evaluation)

    # Finalizing
    with st.spinner('Finalizing...'):
        _, best_solution, best_score = simulate_conversation(N, task, generate_next_message, num_prompts, previous_solutions)
        
    # Display only the best solution and its score
    st.write('Best Solution Found:', best_solution)
    st.write('Score:', best_score)
        
    previous_solutions.append({'solution': best_solution, 'score': best_score})

    if st.button("Run Another Iteration"):
        st.experimental_rerun()