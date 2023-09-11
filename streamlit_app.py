import streamlit as st
from api_setup import setup_api_key
from conversation_simulation import simulate_conversation, generate_prompts, generate_responses, evaluate_responses

def generate_next_message(previous_response):
    return "YOUR_LOGIC_HERE_BASED_ON_previous_response"

st.title("GPT-4 Prompt Optimizer")

task = st.text_area("Enter your task:", "Write a summary of the solar system")
num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=4)

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

    # Create Markdown Table for Evaluation
    st.markdown(evaluation)

    # Prompt selection for the next iteration
    selected_prompt = st.selectbox("Choose the prompt for the next iteration:", generated_prompts, index=0)
    
    # Update task for the next iteration
    task = selected_prompt

    if st.button("Run Another Iteration"):
        st.experimental_rerun()
