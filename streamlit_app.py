import streamlit as st
from conversation_simulation import simulate_conversation, generate_prompts, generate_responses, evaluate_responses

# Initialize session state
if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None

if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []

if 'generated_responses' not in st.session_state:
    st.session_state.generated_responses = []

if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""

st.title("GPT-4 Prompt Optimizer")

# Widgets
task = st.text_area("Enter your task:", "Create ideas for applying Generative AI in a B2B company")
num_prompts = st.slider("Number of Prompts:", min_value=2, max_value=10, value=4)

if st.button("Generate Optimized Prompt"):
    # Stage 1: Generate Prompts
    with st.spinner('Stage 1: Generating Prompts...'):
        st.session_state.generated_prompts = generate_prompts(task, num_prompts, st.session_state.selected_prompt)
    st.write("Generated Prompts:")
    st.write(st.session_state.generated_prompts)

    # Stage 2: Generate Responses
    with st.spinner('Stage 2: Generating Responses...'):
        st.session_state.generated_responses = generate_responses(st.session_state.generated_prompts, task)
    st.write("Generated Responses:")
    st.write(st.session_state.generated_responses)
        
    # Stage 3: Evaluate Responses
    with st.spinner('Stage 3: Evaluating Responses...'):
        st.session_state.evaluation = evaluate_responses(st.session_state.generated_responses, task)
    st.write("Evaluation:")
    st.markdown(st.session_state.evaluation)

# Show radio buttons and button only if prompts have been generated
if st.session_state.generated_prompts:
    st.write("Choose the prompt for the next iteration:")
    st.session_state.selected_prompt = st.radio("", st.session_state.generated_prompts, key='selected_prompt')
    if st.button("Run Another Iteration"):
        st.experimental_rerun()
