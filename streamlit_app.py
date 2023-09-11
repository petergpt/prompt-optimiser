import streamlit as st
from api_setup import setup_api_key
from conversation_simulation import simulate_conversation, generate_prompts, generate_responses, evaluate_responses

# Initialize session state
if 'task' not in st.session_state:
    st.session_state.task = "Write a summary of the solar system"

if 'num_prompts' not in st.session_state:
    st.session_state.num_prompts = 4

if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []

if 'generated_responses' not in st.session_state:
    st.session_state.generated_responses = []

if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""

st.title("GPT-4 Prompt Optimizer")

# Widgets
st.session_state.task = st.text_area("Enter your task:", st.session_state.task)
st.session_state.num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=st.session_state.num_prompts)

if st.button("Generate Optimized Prompt"):
    # Perform one iteration only
    N = 1
    
    # Stage 1: Generate Prompts
    with st.spinner('Stage 1: Generating Prompts...'):
        st.session_state.generated_prompts = generate_prompts(st.session_state.task, st.session_state.num_prompts)
    st.write("Generated Prompts:")
    st.write(st.session_state.generated_prompts)

    # Stage 2: Generate Responses
    with st.spinner('Stage 2: Generating Responses...'):
        st.session_state.generated_responses = generate_responses(st.session_state.generated_prompts, st.session_state.task)
    st.write("Generated Responses:")
    st.write(st.session_state.generated_responses)
        
    # Stage 3: Evaluate Responses
    with st.spinner('Stage 3: Evaluating Responses...'):
        st.session_state.evaluation = evaluate_responses(st.session_state.generated_responses, st.session_state.task)
    st.write("Evaluation:")
    st.markdown(st.session_state.evaluation)
    
# Display the radio buttons even if the button hasn't been clicked yet
st.write("Choose the prompt for the next iteration:")
selected_prompt = st.radio("", st.session_state.generated_prompts)

# Update task for the next iteration
if selected_prompt:
    st.session_state.task = selected_prompt

if st.button("Run Another Iteration"):
    st.experimental_rerun()
