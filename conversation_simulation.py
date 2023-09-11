import streamlit as st
from api_setup import setup_api_key

# Initialize session state
if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None

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

# Create empty placeholders for radio and button
radio_placeholder = st.empty()
button_placeholder = st.empty()

if st.button("Generate Optimized Prompt"):
    N = 1
    initial_prompt = st.session_state.selected_prompt if st.session_state.selected_prompt else st.session_state.task

    # Stage 1: Generate Prompts
    with st.spinner('Stage 1: Generating Prompts...'):
        st.session_state.generated_prompts = generate_prompts(initial_prompt, st.session_state.num_prompts, task=st.session_state.task)
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

# Populate the placeholders if results are available
if st.session_state.generated_prompts:
    radio_placeholder.write("Choose the prompt for the next iteration:")
    st.session_state.selected_prompt = radio_placeholder.radio("", st.session_state.generated_prompts)
    if button_placeholder.button("Run Another Iteration"):
        st.experimental_rerun()
